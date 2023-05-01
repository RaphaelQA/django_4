from django.urls import path

from ads.views import UserCreateView, UserDetailView, UserDeleteView, UserListUpdateView,UserListView


urlpatterns = [
    path('', UserListView.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
    path('create/', UserCreateView.as_view()),
    path('<int:pk>/update/', UserListUpdateView.as_view()),
    path('<int:pk>/delete/', UserDeleteView.as_view()),
]