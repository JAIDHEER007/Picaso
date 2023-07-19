from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'gallery'
urlpatterns = [
    path('', views.showGallery, name='showGallery'),
    path('<str:img_uid>/', views.showImage, name='showImage'),
]
