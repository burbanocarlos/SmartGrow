"""
Contents:
    • Index View
    • Device-related views
    • TP-Link Kasa device views
    • DRF authentication view
    • Climate Control functionality

"""

from datetime import datetime
import asyncio
import json
import requests

# Standard library imports
from datetime import datetime
import asyncio
import json

# Third-party imports
from asgiref.sync import sync_to_async
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from tplinkcloud import TPLinkDeviceManager
from firebase_admin import db

# Local imports
from .forms import ClimateControlSettingsForm
from .models import ClimateControlSettings, Device, SensorData
from .decorators import async_login_required

# ----------------------------
# Index view
# ----------------------------
@login_required
def index(request):
    return render(request, 'smart_grow/index.html')

# ----------------------------
# Device-related views
# ----------------------------
def devices_list(request):
    devices = Device.objects.all()
    context = {'devices': devices}
    return render(request, 'smart_grow/devices_list.html', context)

@login_required
def device_info(request):
    data = SensorData.objects.first()
    if data:
        context = {
                'device_name': data.device_name,
                'current_temperature': data.temperature,
                'current_humidity': data.humidity,
                'time_stamp' : data.timestamp
            }
    else:
        context = {
                'device_name': "None",
                'current_temperature': "none",
                'current_humidity': -1,
                'time_stamp' : -1
            }
    return render(request, 'smart_grow/device_info.html', context)
    
@api_view(['POST'])
def store_device_info(request):
    data = request.data
    device_name = data['device_name']
    temperature = data['temperaure']
    humidity = data['humidity']
    time_stamp = data['time_stamp']

    reading = SensorData(device_name=device_name, temperature=temperature, humidity=humidity, timestamp=time_stamp)
    reading.save()

    return Response({'status' : 'success'}, status=200)

# ----------------------------
# TP-Link Kasa device views
# ----------------------------
TPLINK_USERNAME = settings.TPLINK_USERNAME
TPLINK_PASSWORD = settings.TPLINK_PASSWORD

async def get_device_info(device):
    device_data = {
        "model_type": device.model_type.name,
        "alias": device.get_alias(),
        "device_info": json.loads(json.dumps(device.device_info, indent=2, default=lambda x: vars(x)
                        if hasattr(x, "__dict__") else x.name if hasattr(x, "name") else None)),
        "sys_info": json.loads(json.dumps(await device.get_sys_info(), indent=2, default=lambda x: vars(x)
                        if hasattr(x, "__dict__") else x.name if hasattr(x, "name") else None))
    }
    return device_data

async def get_tplink_cloud_devices(device_manager):
    devices = await device_manager.get_devices()
    tasks = [get_device_info(device) for device in devices]
    results = await asyncio.gather(*tasks)
    return results

def get_tplink_device_manager():
    return TPLinkDeviceManager(TPLINK_USERNAME, TPLINK_PASSWORD)

@async_login_required()
async def async_kasa_devices(request):
    device_manager = TPLinkDeviceManager(TPLINK_USERNAME, TPLINK_PASSWORD) 
    devices = await get_tplink_cloud_devices(device_manager)
    devices_to_ignore = ["UNKNOWN", "KP303", "KP303CHILD"]
    device_info = [{"alias": device.get('alias'), "device_model": device.get('model_type'), "relay_state": device.get('sys_info', {}).get('relay_state')} for device in devices if device.get('model_type') not in devices_to_ignore and device.get('sys_info') is not None]
    return device_info

@async_login_required()
async def kasa_devices(request):
    device_info = await async_kasa_devices(request)
    context = {"kasa_devices": device_info}
    return render(request, "smart_grow/kasa_devices_api.html", context)

# ----------------------------
# DRF authentication view
# ----------------------------
class MySecureView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {'message': 'Hello, authenticated user!'}
        return Response(content)

# ----------------------------
# Climate Control functionality
# ----------------------------
# @async_login_required()
async def update_climate_control_settings(request):
    
    settings = await sync_to_async(ClimateControlSettings.objects.first)()
    device_info = await async_kasa_devices(request)
    form = ClimateControlSettingsForm(request.POST or None, instance=settings, device_info=device_info)    
    print(device_info)
    success = False
    if form.is_valid():
        await sync_to_async(form.save)()
        await sync_to_async(post_thresholds)()
        success = True

    context = {'form': form, 'success': success}
    return render(request, 'smart_grow/climate_control_settings.html', context)

def post_thresholds():
    settings = ClimateControlSettings.objects.first()
    data = {
        'temperature' : {
            'temperature_threshold': settings.temperature_threshold,
            'device_1' : settings.device_1,
        },
        'humidity' : {
            'humidity_threshold': settings.humidity_threshold,
            'device_2' : settings.device_2
            }
    }
    # Set the trigger command in Firebase
    threshols_ref = db.reference("/thresholds")
    threshols_ref.set(data)

def get_thresholds(request):
    settings = ClimateControlSettings.objects.first()
    data = {
        'temperature_threshold': settings.temperature_threshold,
        'humidity_threshold': settings.humidity_threshold,
        'device_1' : settings.device_1,
        'device_2' : settings.device_2
    }
    return JsonResponse(data)

