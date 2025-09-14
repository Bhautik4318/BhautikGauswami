from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('debug/', views.debug_images, name='debug_images'),
    path('test/', views.url_test, name='url_test'),
]
