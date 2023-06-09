# Generated by Django 4.2 on 2023-05-02 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smart_grow', '0005_alter_climatecontrolsettings_device_1_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sensordata',
            old_name='value',
            new_name='humidity',
        ),
        migrations.AddField(
            model_name='sensordata',
            name='device_name',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='smart_grow.device'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sensordata',
            name='temperature',
            field=models.FloatField(default=-1),
            preserve_default=False,
        ),
    ]
