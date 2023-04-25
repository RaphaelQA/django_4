import json

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Category, Ad, User, Location


# Create your views here.

def root(request):
    return JsonResponse({'status': 'ok'})


@method_decorator(csrf_exempt, name='dispatch')
class Category_List_Create_View(CreateView):
    model = Category
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        new_cat = Category.objects.create(name=data.get('name'))
        return JsonResponse({
            'id': new_cat.pk,
            'name': new_cat.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class Category_List_Viev(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return JsonResponse([{'id': cat.pk, 'name': cat.name} for cat in self.object_list.order_by('name')], safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class Category_Datail_View(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        cat = self.get_object()
        return JsonResponse({
            'id': cat.pk,
            'name': cat.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class Category_List_Update_View(UpdateView):
    model = Category
    fields = '__all__'

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        self.object.name = data.get('name')

        return JsonResponse({
            'id': self.object.pk,
            'name': self.object.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class Category_List_Delete_View(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({
            'success': 'ok'}, status=204)


############################################################

@method_decorator(csrf_exempt, name='dispatch')
class Ad_List_Create_View(CreateView):
    model = Ad
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        author = get_object_or_404(User, pk=data.pop('author_id'))
        category = get_object_or_404(Category, pk=data.pop('category_id'))

        ad = Ad.objects.create(author_id=author, category_id=category, **data)
        return JsonResponse({
            'id': ad.pk,
            'name': ad.name,
            'price': ad.price,
            'author': ad.author_id.username,
            'description': ad.description,
            'category': ad.category_id.name,
            'is_published': ad.is_published,
            'image': ad.image.url if ad.image else None
        })


@method_decorator(csrf_exempt, name='dispatch')
class Ad_List_Viev(ListView):
    model = Ad
    object_on_pages = 5

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list.order_by('-price'), self.object_on_pages)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return JsonResponse({
            'total': paginator.count,
            'num_pages': paginator.num_pages,
            'items': [{'id': ad.pk,
                       'name': ad.name,
                       'price': ad.price,
                       'author': ad.author_id.username,
                       'description': ad.description,
                       'category': ad.category_id.name,
                       'is_published': ad.is_published,
                       'image': ad.image.url if ad.image else None
                       } for ad in page_obj]}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class Ad_Datail_View(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        return JsonResponse({
            'id': ad.pk,
            'name': ad.name,
            'price': ad.price,
            'author': ad.author_id.username,
            'description': ad.description,
            'category': ad.category_id.name,
            'is_published': ad.is_published,
            'image': ad.image.url if ad.image else None
        })


@method_decorator(csrf_exempt, name='dispatch')
class Ad_List_Update_View(UpdateView):
    model = Ad
    fields = '__all__'

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        if 'name' in data:
            self.object.name = data.get('name')

        if 'description' in data:
            self.object.name = data.get('name')

        if 'price' in data:
            self.object.name = data.get('price')

        if 'category_id' in data:
            category = get_object_or_404(Category, pk=data.get('category_id'))
            self.object.category = category

        return JsonResponse({
            'id': self.object.pk,
            'name': self.object.name,
            'price': self.object.price,
            'author': self.object.author_id.username,
            'description': self.object.description,
            'category': self.object.category_id.name,
            'is_published': self.object.is_published,
            'image': self.object.image.url if self.object.image else None})


@method_decorator(csrf_exempt, name='dispatch')
class Ad_List_Delete_View(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'success': 'ok'}, status=204)


@method_decorator(csrf_exempt, name='dispatch')
class Ad_UploadImage_View(UpdateView):
    model = Ad
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        self.object.image = request.FILES.get('image')
        self.object.save()
        return JsonResponse({
            'id': self.object.pk,
            'name': self.object.name,
            'price': self.object.price,
            'author': self.object.author_id.username,
            'description': self.object.description,
            'category': self.object.category_id.name,
            'is_published': self.object.is_published,
            'image': self.object.image.url
        })


#####################################################################################

@method_decorator(csrf_exempt, name='dispatch')
class User_List_Create_View(CreateView):
    model = User
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        locations = data.pop('locations')
        user = User.objects.create(**data)
        for loc_name in locations:
            loc, _ = Location.objects.get_or_create(name=loc_name)
            user.locations.add(loc)
        user.save()

        return JsonResponse({
            'id': user.pk,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "age": user.age,
            "locations": [loc.name for loc in user.locations.all()]
        })


@method_decorator(csrf_exempt, name='dispatch')
class User_List_Viev(ListView):
    queryset = User.objects.annotate(total_ads=Count('ad', filter=Q(ad__is_published=True))).order_by('username')
    model = User
    object_on_pages = 5

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list.order_by('username'), self.object_on_pages)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return JsonResponse({
            'total': paginator.count,
            'num_pages': paginator.num_pages,
            'items': [{'id': user.pk,
                       "first_name": user.first_name,
                       "last_name": user.last_name,
                       "username": user.username,
                       "role": user.role,
                       "age": user.age,
                       "locations": [loc.name for loc in user.locations.all()],
                       'total_ads': user.total_ads
                       } for user in page_obj]}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class User_Datail_View(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return JsonResponse({
            'id': user.pk,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "age": user.age,
            "locations": [loc.name for loc in user.locations.all()]})


@method_decorator(csrf_exempt, name='dispatch')
class User_List_Update_View(UpdateView):
    model = User
    fields = '__all__'

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        if 'first_name' in data:
            self.object.first_name = data.get('first_name')

        if 'username' in data:
            self.object.username = data.get('username')

        if 'last_name' in data:
            self.object.last_name = data.get('last_name')

        if 'age' in data:
            self.object.age = data.get('age')

        if 'locations' in data:
            self.object.locations.clear()
            for loc_name in data.get('locations'):
                loc, _ = Location.objects.get_or_create(name=loc_name)
                self.object.locations.add(loc)

        return JsonResponse({
            'id': self.object.pk,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "role": self.object.role,
            "age": self.object.age,
            "locations": [loc.name for loc in self.object.locations.all()]})


@method_decorator(csrf_exempt, name='dispatch')
class User_List_Delete_View(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'success': 'ok'}, status=204)
