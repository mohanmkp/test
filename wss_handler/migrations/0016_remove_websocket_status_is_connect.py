# Generated by Django 4.1.3 on 2023-01-10 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wss_handler', '0015_websocket_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='websocket_status',
            name='is_connect',
        ),
    ]
