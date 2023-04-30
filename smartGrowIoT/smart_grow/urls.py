
from django.urls import path, include
from . import views
from .views import MySecureView, APIView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

from django.contrib.auth import views as auth_views
from django.urls import re_path
from django.contrib import admin
#from .views import MyApiView


app_name = 'smart_grow'
urlpatterns = [
    path('', views.index, name='index'),
    path('devices/', views.devices_list, name='devices_list'),
    path('sensor_data/', views.sensor_data_list, name='sensor_data_list'),
    path('device_info/', views.device_info, name='device_info'),
    path('kasa_devices/', views.kasa_devices, name='kasa_devices'),
    path('secure/', MySecureView.as_view(), name='secure'),
    path('login/', LoginView.as_view(template_name='smart_grow/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('climate-control-settings/', views.update_climate_control_settings, name='climate_control_settings'),

    
]


