from django.db import models

class Sensor(models.Model):
    name = models.CharField(max_length=100)
    sensor_type = models.CharField(max_length=50)
    value = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    
class Device(models.Model):
    name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=50)
    device_id = models.CharField(max_length=100, unique=True)
    is_online = models.BooleanField(default=False)
    battery_level = models.IntegerField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    device_location = models.CharField(max_length=255, default="Unknown")

    def __str__(self):
        return self.name

class KasaDevice(models.Model):
    name = models.CharField(max_length=100)
    kasa_device_id = models.CharField(max_length=100, unique=True)
    is_online = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class DeviceSensor(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.device.name} - {self.sensor.name}"

class SensorData(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sensor.name} - {self.value} - {self.timestamp}"


