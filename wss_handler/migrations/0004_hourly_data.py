# Generated by Django 4.1.3 on 2023-01-05 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wss_handler', '0003_ws_sessions_logout_ws_sessions_logout_on_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hourly_Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received_on', models.DateTimeField(auto_now=True)),
                ('data', models.CharField(max_length=255)),
                ('message_type', models.CharField(max_length=2)),
                ('aws_date', models.CharField(max_length=6)),
                ('aws_time', models.CharField(max_length=2)),
                ('station_id', models.CharField(max_length=5)),
                ('transmission_mode', models.CharField(max_length=2)),
                ('packet_data', models.CharField(max_length=117)),
            ],
        ),
    ]