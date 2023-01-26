from django.urls import path

from . import views

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('menu2/', views.menu, name='menu2'),
    path('menu/submenu/', views.menu, name='submenu'),
    path('menu/category/', views.menu, name='category'),
    path('menu/category2/', views.menu, name='category2'),
    path('menu/category/subcategory', views.menu, name='subcategory'),
]