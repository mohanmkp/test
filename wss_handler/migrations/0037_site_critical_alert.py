# Generated by Django 4.1.3 on 2023-02-02 08:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wss_handler', '0036_weather_forecast_message_packet'),
    ]

    operations = [
        migrations.CreateModel(
            name='site_critical_alert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_on', models.DateTimeField(auto_now=True)),
                ('json_data', models.JSONField(blank=True, null=True)),
                ('sequence_num', models.IntegerField()),
                ('ack', models.BooleanField(blank=True, null=True)),
                ('start_date', models.CharField(max_length=6)),
                ('grid_id', models.CharField(max_length=4)),
                ('packet', models.CharField(max_length=255)),
                ('num_of_day', models.CharField(max_length=2)),
                ('avalanche_axis_id', models.CharField(max_length=3)),
                ('alert_message', models.TextField(max_length=100)),
                ('send_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
