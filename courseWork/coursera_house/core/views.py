from django.urls import reverse_lazy
from django.views.generic import FormView
from django.conf import settings

from .models import Setting
from .tasks import get_sensors_data, parse_sensors_data
from .form import ControllerForm


def get_controller(controller_name):
    try:
        controller = Setting.objects.get(controller_name=controller_name)
    except (Setting.DoesNotExist, Setting.MultipleObjectsReturned):
        return None
    return controller


def get_or_create_controller(controller_name, label=''):
    try:
        controller = Setting.objects.get(controller_name=controller_name)
    except Setting.DoesNotExist:
        controller = Setting(controller_name=controller_name, label=label)
        controller.save()
    except Setting.MultipleObjectsReturned:
        temp = Setting.objects.all()
        temp[1:].delete()
        return temp[0]
    return controller


class ControllerView(FormView):
    form_class = ControllerForm
    template_name = 'core/control.html'
    success_url = reverse_lazy('form')
    controller_names = {'bedroom_target_temperature' : 'Желаемая температура в спальне',
                        'hot_water_target_temperature': 'Желаемая температура горячей воды',
                        'bedroom_light': 'свет в спальне',
                        'bathroom_light': 'свет в ванной'}

    def get_context_data(self, **kwargs):

        data = get_sensors_data(settings.SMART_HOME_API_URL, settings.SMART_HOME_ACCESS_TOKEN)
        parsed_data = parse_sensors_data(data)
        context = super(ControllerView, self).get_context_data()
        context['data'] = parsed_data
        return context

    def get_initial(self):
        initial = {}

        for controller in self.controller_names.keys():
            initial_target_value = get_controller(controller)
            if initial_target_value is not None:
                initial[controller] = initial_target_value.value
                if controller == 'bedroom_light' or controller == 'bathroom_light':
                    initial[controller] = bool(initial[controller])
        return initial

    def form_valid(self, form):
        if form.is_valid():
            for controller_name in self.controller_names.keys():
                controller = get_or_create_controller(controller_name, label=self.controller_names[controller_name])
                controller.value = int(form.cleaned_data[controller_name])
                controller.save()
        return super(ControllerView, self).form_valid(form)
