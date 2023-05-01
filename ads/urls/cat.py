from django.urls import path

from ads.views import CategoryListCreateView, CategoryDatailView, CategoryListDeleteView, \
CategoryListUpdateView, CategoryListViev


urlpatterns = [
    path('', CategoryListViev.as_view()),
    path('<int:pk>/', CategoryDatailView.as_view()),
    path('create/', CategoryListCreateView.as_view()),
    path('<int:pk>/update/', CategoryListUpdateView.as_view()),
    path('<int:pk>/delete/', CategoryListDeleteView.as_view()),
]