from django.urls import path

from ads.views import Ad_Datail_View, Ad_List_Create_View, Ad_List_Delete_View, Ad_List_Update_View, Ad_List_Viev, Ad_UploadImage_View


urlpatterns = [
    path('', Ad_List_Viev.as_view()),
    path('<int:pk>/', Ad_Datail_View.as_view()),
    path('create/', Ad_List_Create_View.as_view()),
    path('<int:pk>/update/', Ad_List_Update_View.as_view()),
    path('<int:pk>/delete/', Ad_List_Delete_View.as_view()),
    path('<int:pk>/upload_image/', Ad_UploadImage_View.as_view()),
]