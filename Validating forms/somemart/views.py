import json
from django.forms.models import model_to_dict
from django.core import serializers

from django.http import HttpResponse, JsonResponse, Http404
from django.views import View
from django import forms

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Item, Review


class CreateItemForm(forms.Form):
    title =  forms.CharField(required=True,  max_length=64)
    description = forms.CharField(required=True,  max_length=1024)
    price = forms.IntegerField(required=True, min_value=1, max_value=1000000)

    def clean_description(self):
        if type(self.data['description']) is int :
            raise forms.ValidationError('description cant be a number!')
        return self.cleaned_data['description']

    def clean_title(self):
        if type(self.data['title']) is int :
            raise forms.ValidationError('title cant be a number!')
        return self.cleaned_data['title']

class CreateReviewForm(forms.Form):
    grade = forms.IntegerField(required=True, min_value=1, max_value=10)
    text = forms.CharField(required=True, max_length=1024)


    def clean_text(self):
        if type(self.data['text']) is int :
            raise forms.ValidationError('text cant be a number!')
        return self.cleaned_data['text']


@method_decorator(csrf_exempt, name='dispatch')
class AddItemView(View):
    """View для создания товара."""


    def post(self, request):
        # Здесь должен быть ваш код
        try:
            received_json_data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse(status=400)
        print(received_json_data)
        form = CreateItemForm(received_json_data)

        if form.is_valid():
            data = form.cleaned_data
            item = Item(title = data['title'], description= data['description'], price = data['price'])
            item.save()


            return JsonResponse(data={'id':item.pk}, status=201)
        else:
            return HttpResponse(status=400)




@method_decorator(csrf_exempt, name='dispatch')
class PostReviewView(View):
    """View для создания отзыва о товаре."""

    def post(self, request, item_id):

        try:
            received_json_data = json.loads(request.body)
            item = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            raise Http404()
        except json.JSONDecodeError:
            return HttpResponse(status=400)


        form = CreateReviewForm(received_json_data)

        if form.is_valid():
            data = form.cleaned_data

            review = Review(grade = data['grade'], text = data['text'], item = item)
            review.save()
            return JsonResponse(data={'id': review.pk}, status=201)
        else:
            return HttpResponse(status=400)




class GetItemView(View):
    """View для получения информации о товаре.

    Помимо основной информации выдает последние отзывы о товаре, не более 5
    штук.
    """

    def get(self, request, item_id):
        item = None
        try:
            item = Item.objects.get(pk = item_id)
        except Item.DoesNotExist:
            raise Http404()

        reviews = Review.objects.filter(item_id= item.pk).order_by('-id')[:5]

        serialized_item = model_to_dict(item)
        serialized_reviews = list(map(lambda r: model_to_dict(r,fields=('id','text','grade')), reviews))
        serialized_item['reviews'] = serialized_reviews




        return JsonResponse(data=serialized_item,safe=False,  status=200)
