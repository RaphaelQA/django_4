from django.urls import path

from ads.views import CategoryListCreateView, CategoryDetailView, CategoryListDeleteView, \
CategoryListUpdateView, CategoryListView


urlpatterns = [
    path('', CategoryListView.as_view()),
    path('<int:pk>/', CategoryDetailView.as_view()),
    path('create/', CategoryListCreateView.as_view()),
    path('<int:pk>/update/', CategoryListUpdateView.as_view()),
    path('<int:pk>/delete/', CategoryListDeleteView.as_view()),
]