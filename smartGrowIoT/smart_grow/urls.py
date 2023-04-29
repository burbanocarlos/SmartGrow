
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
    path('add_device/', views.add_device, name='add_device'),
    #path('kasa_devices/', views.kasa_devices_list, name='kasa_devices_list'), this is the old ones we need to delete
    path('sensor_data/', views.sensor_data_list, name='sensor_data_list'),
    path('kasa_device/<int:kasa_device_id>/', views.kasa_device_detail, name='kasa_device_detail'),
    path('device_info/', views.device_info, name='device_info'),
    path('kasa_devices/', views.kasa_devices, name='kasa_devices'),
    path('secure/', MySecureView.as_view(), name='secure'),
    #path('my-api-view/', MyApiView.as_view(), name='my_api_view'),

    #path('devices/<int:device_id>/edit/', views.edit_device, name='edit_device'),
    #path('devices/<int:device_id>/delete/', views.delete_device, name='delete_device'),
]


