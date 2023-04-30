from datetime import datetime
import asyncio
import json
import pytz
import requests

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.shortcuts import render

from .forms import ClimateControlSettingsForm
from .models import ClimateControlSettings
from .models import Device, KasaDevice, DeviceSensor, SensorData
from .decorators import async_login_required
from tplinkcloud import TPLinkDeviceManager
from kasa import Discover



@login_required
def index(request):
    return render(request, 'smart_grow/index.html')

"""
This view retrieves all the devices from the database, puts them in a 
context dictionary, and renders a template called devices_list.html that
will display the list of devices.
"""
def devices_list(request):
    devices = Device.objects.all()
    context = {'devices': devices}
    return render(request, 'smart_grow/devices_list.html', context)
"""
we are keeping this function 
"""
@login_required
def device_info(request):
    esp32_ip = fetch_ip_address()  # Replace with the IP address of your ESP32
    url = f"http://{esp32_ip}/device_info"
    try:
        response = requests.get(url, timeout=2)
        data = response.json()
        context = {
            'device_name': data['device_name'],
            'wifi_status': data['wifi_status'],
            'current_temperature': data['current_temperature'],
            'current_humidity': data['current_humidity'],
        }
    except requests.exceptions.Timeout:
        context = {'message': 'Could not connect to device'}
    
    return render(request, 'smart_grow/device_info.html', context)

"""
up to here 
"""
"""
this is for the new way to fetching kasa devices, the other part will most leikely be deleted at some point
this is acccesign the tp cloud api, this way even if we are not in the same network we can still control our
devices
"""
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
async def kasa_devices(request):
    device_manager = TPLinkDeviceManager(TPLINK_USERNAME, TPLINK_PASSWORD) 
    devices = await get_tplink_cloud_devices(device_manager)
    devices_to_ignore = ["UNKNOWN", "KP303", "KP303CHILD"]
    device_info = [{"alias": device.get('alias'), "device_model": device.get('model_type'), "relay_state": device.get('sys_info', {}).get('relay_state')} for device in devices if device.get('model_type') not in devices_to_ignore and device.get('sys_info') is not None]

    context = {"kasa_devices": device_info}
    return render(request, "smart_grow/kasa_devices_api.html", context)

"""
this ends the new way to fetch kasa devices
"""

#fetch sensor data from ThinkSpeak
def fetch_sensor_data():
    api_key = 'EHN8P66QEUONM1NJ'
    
    channel_id = '2125746'
    url = f'https://api.thingspeak.com/channels/{channel_id}/feeds.json?api_key={api_key}&results=10'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


#fetch the ip address of the esp32 board from thinkspeak 
def fetch_ip_address():
    api_key = 'EHN8P66QEUONM1NJ'
    channel_id = '2125746'
    url = f"https://api.thingspeak.com/channels/{channel_id}/fields/3/last.json?api_key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        ip_address = data["field3"]
        return ip_address
    else:
        return None


from django.shortcuts import render

def sensor_data_list(request):
    sensor_data = fetch_sensor_data()

    if sensor_data:
        # Extracting sensor values from JSON response
        feeds = sensor_data['feeds']
        temperature_values = [float(feed['field1']) for feed in feeds]

        # Convert timestamp strings to datetime objects
        utc_time_stamp = [datetime.strptime(feed['created_at'], '%Y-%m-%dT%H:%M:%SZ') for feed in feeds]

        # Set timezone objects
        utc = pytz.timezone('UTC')
        cst = pytz.timezone('America/Chicago')

        # Convert timestamps to Central Standard Time
        time_stamp = [utc.localize(dt).astimezone(cst).strftime('%Y-%m-%d %H:%M:%S') for dt in utc_time_stamp]

        humidity_values = [float(feed['field2']) for feed in feeds]

        zipped_data = zip(temperature_values, humidity_values, time_stamp)

        context = {
            'zipped_data': zipped_data
        }
    else:
        context = {}

    return render(request, 'smart_grow/sensor_data_list.html', context)

"""
here we start our view for the DRF authentication 
"""

class MySecureView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {'message': 'Hello, authenticated user!'}
        return Response(content)
    

"""
here we start the climateControl functionality
"""



def update_climate_control_settings(request):
    settings = ClimateControlSettings.objects.first()
    form = ClimateControlSettingsForm(request.POST or None, instance=settings)
    
    if form.is_valid():
        form.save()
    
    context = {'form': form}
    return render(request, 'smart_grow/climate_control_settings.html', context)


