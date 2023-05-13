import json

from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.ad_serializer import AdListSerializer, AdDetailSerializer, AdDestroySerializer, AdCreateSerializer, \
    AdUpdateSerializer
from ads.cat_serialiazer import CatListSerializer, CatCreateSerializer
from ads.models import Category, Ad, User, Location
from ads.user_serializers import UserDetailSerializer, UserCreateSerializer, UserDestroySerializer, \
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


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CatListSerializer


class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CatListSerializer


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


class CategoryListDeleteView(DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CatCreateSerializer


############################################################


class AdListCreateView(CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer


class AdPagination(PageNumberPagination):
    page_size = 5


class AdListView(ListAPIView):
    queryset = Ad.objects.all().order_by('id')
    serializer_class = AdListSerializer
    pagination_class = AdPagination

    def get(self, request, *args, **kwargs):
        ad_text = request.GET.get('text', None)
        if ad_text:
            self.queryset = self.queryset.filter(name__icontains=ad_text)

        cat_id = request.GET.get("cat")
        if cat_id:
            self.queryset = self.queryset.filter(category_id__in=cat_id)

        location = request.GET.get('location')
        if location:
            self.queryset = self.queryset.filter(author__locations__name__icontains=location)

        price_from = request.GET.get('price_from')
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)

        price_to = request.GET.get('price_to')
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)
        return super().get(request, *args, **kwargs)


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    permission_classes = [IsAuthenticated]


class AdListUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdUpdateSerializer


class AdListDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDestroySerializer


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


class UserPagination(PageNumberPagination):
    page_size = 5


class UserListView(ListAPIView):
    queryset = User.objects.annotate(total_ads=Count('ad', filter=Q(ad__is_published=True))).order_by('username')
    serializer_class = UserListSerializer
    pagination_class = UserPagination


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
