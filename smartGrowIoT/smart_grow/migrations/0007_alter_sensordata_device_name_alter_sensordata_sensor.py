# Generated by Django 4.2 on 2023-05-02 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smart_grow', '0006_rename_value_sensordata_humidity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensordata',
            name='device_name',
            field=models.ForeignKey(default='None', on_delete=django.db.models.deletion.CASCADE, to='smart_grow.device'),
        ),
        migrations.AlterField(
            model_name='sensordata',
            name='sensor',
            field=models.ForeignKey(default='None', on_delete=django.db.models.deletion.CASCADE, to='smart_grow.sensor'),
        ),
    ]