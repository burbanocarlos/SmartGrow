from django import forms
from .models import Device
from .models import ClimateControlSettings

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name', 'device_type', 'device_id', 'device_location']


class ClimateControlSettingsForm(forms.ModelForm):
    class Meta:
        model = ClimateControlSettings
        fields = ['temperature_threshold', 'humidity_threshold']
