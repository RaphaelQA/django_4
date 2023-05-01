import json

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet

from ads.models import Category, Ad, User, Location
from ads.serializers import UserDetailSerializer, UserCreateSerializer, UserDestroySerializer, \
    UserUpdateSerializer, UserListSerializer, LocationSerializer


# Create your views here.

def root(request):
    return JsonResponse({'status': 'ok'})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListCreateView(CreateView):
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
class CategoryListViev(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return JsonResponse([{'id': cat.pk, 'name': cat.name} for cat in self.object_list.order_by('name')], safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDatailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        cat = self.get_object()
        return JsonResponse({
            'id': cat.pk,
            'name': cat.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListUpdateView(UpdateView):
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
class CategoryListDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({
            'success': 'ok'}, status=204)


############################################################

@method_decorator(csrf_exempt, name='dispatch')
class AdListCreateView(CreateView):
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
class AdListView(ListView):
    model = Ad
    # object_on_pages = 20

    # def get(self, request, *args, **kwargs):
        # super().get(request, *args, **kwargs)
        #
        # paginator = Paginator(self.object_list.order_by('-price'), self.object_on_pages)
        # page_number = request.GET.get('page')
        # page_obj = paginator.get_page(page_number)
        #
        # return JsonResponse({
        #     'total': paginator.count,
        #     'num_pages': paginator.num_pages,
        #     'items': [{'id': ad.pk,
        #                'name': ad.name,
        #                'price': ad.price,
        #                'author': ad.author_id.username,
        #                'description': ad.description,
        #                'category': ad.category_id.name,
        #                'is_published': ad.is_published,
        #                'image': ad.image.url if ad.image else None
        #                } for ad in page_obj]}, safe=False)

    def get(self, request, *args, **kwargs):
        ad_text = request.GET.get('text', None)
        if ad_text:
            self.queryset = self.queryset.filter(
                text__icontains=ad_text
            )
        cat_id = request.GET.get("cat", None)
        if cat_id:
            self.queryset = self.queryset.filter(
                categogory__id__icontains=cat_id
            )
        return super().get(request, *args, **kwargs)
@method_decorator(csrf_exempt, name='dispatch')
class AdDetailView(DetailView):
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
class AdListUpdateView(UpdateView):
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
class AdListDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'success': 'ok'}, status=204)


@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImageView(UpdateView):
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

class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    object_on_pages = 5

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.queryset.order_by('username'), self.object_on_pages)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return JsonResponse({
            'total': paginator.count,
            'num_pages': paginator.num_pages,
            'items': UserListSerializer(page_obj, many=True).data})



class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserListUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer

class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDestroySerializer

class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer