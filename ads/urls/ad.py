from django.urls import path

from ads.views import AdDetailView, AdListCreateView, AdListDeleteView, AdListUpdateView, AdListView, AdUploadImageView


urlpatterns = [
    path('', AdListView.as_view()),
    path('<int:pk>/', AdDetailView.as_view()),
    path('create/', AdListCreateView.as_view()),
    path('<int:pk>/update/', AdListUpdateView.as_view()),
    path('<int:pk>/delete/', AdListDeleteView.as_view()),
    path('<int:pk>/upload_image/', AdUploadImageView.as_view()),
]