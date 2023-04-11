import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Category, Ad


# Create your views here.

def root(request):
    return JsonResponse({'status': 'ok'})


@method_decorator(csrf_exempt, name='dispatch')
class Category_List_Create_View(View):
    def get(self, request):
        categories = Category.objects.all()
        return JsonResponse([{
            'id': cat.pk,
            'name': cat.name
        }for cat in categories], safe=False)

    def post(self, request):
        data = json.loads(request.body)
        new_cat = Category.objects.create(name=data.get('name'))
        return JsonResponse({
            'id': new_cat.pk,
            'name': new_cat.name
        })


class Category_DateView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        cat = self.get_object()
        return JsonResponse({
            'id': cat.pk,
            'name': cat.name
        })



@method_decorator(csrf_exempt, name='dispatch')
class Ad_List_Create(View):
    def get(self, request):
        categories = Ad.objects.all()
        return JsonResponse([{
            'id': ad.pk,
            'name': ad.name,
            'price': ad.price,
            'author': ad.author,
            'description': ad.description,
            'address': ad.address,
            'is_published': ad.is_published
        }for ad in categories], safe=False)

    def post(self, request):
        data = json.loads(request.body)
        ad = Ad.objects.create(**data)
        return JsonResponse({
            'id': ad.pk,
            'name': ad.name,
            'price': ad.price,
            'author': ad.author,
            'description': ad.description,
            'address': ad.address,
            'is_published': ad.is_published
        })


class Ad_DateView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        return JsonResponse({
            'id': ad.pk,
            'name': ad.name,
            'price': ad.price,
            'author': ad.author,
            'description': ad.description,
            'address': ad.address,
            'is_published': ad.is_published
        })


