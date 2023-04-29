
from django.urls import path, include
from . import views
from .views import MySecureView, APIView
from django.urls import re_path
from django.contrib import admin
#from .views import MyApiView


app_name = 'smart_grow'
urlpatterns = [
    path('', views.index, name='index'),
    path('devices/', views.devices_list, name='devices_list'),
    path('devices/<int:device_id>/', views.device_detail, name='device_detail'),
    path('sensor_data/', views.sensor_data_list, name='sensor_data_list'),
    path('device_info/', views.device_info, name='device_info'),
    path('kasa_devices/', views.kasa_devices, name='kasa_devices'),
    path('secure/', MySecureView.as_view(), name='secure'),
]


