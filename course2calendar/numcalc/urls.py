from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload-html/', views.upload_html, name='upload_html'),
] 