from django import forms


class ControllerForm(forms.Form):
    bedroom_target_temperature = forms.IntegerField(initial= 21, min_value=16, max_value=51)
    hot_water_target_temperature = forms.IntegerField(initial= 80, min_value=24, max_value=90)
    bedroom_light = forms.BooleanField(required=False)
    bathroom_light = forms.BooleanField(required=False)
