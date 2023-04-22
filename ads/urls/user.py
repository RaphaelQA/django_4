from django.urls import path

from ads.views import User_List_Create_View, User_Datail_View, User_List_Delete_View, User_List_Update_View,User_List_Viev


urlpatterns = [
    path('', User_List_Viev.as_view()),
    path('<int:pk>/', User_Datail_View.as_view()),
    path('create/', User_List_Create_View.as_view()),
    path('<int:pk>/update/', User_List_Update_View.as_view()),
    path('<int:pk>/delete/', User_List_Delete_View.as_view()),
]