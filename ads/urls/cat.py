from django.urls import path

from ads.views import Category_List_Create_View, Category_Datail_View, Category_List_Delete_View, \
Category_List_Update_View, Category_List_Viev


urlpatterns = [
    path('', Category_List_Viev.as_view()),
    path('<int:pk>/', Category_Datail_View.as_view()),
    path('create/', Category_List_Create_View.as_view()),
    path('<int:pk>/update/', Category_List_Update_View.as_view()),
    path('<int:pk>/delete/', Category_List_Delete_View.as_view()),
]