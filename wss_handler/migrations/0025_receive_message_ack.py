# Generated by Django 4.1.3 on 2023-01-19 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wss_handler', '0024_query_send_message_ack_ws_sessions_log_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='receive_message',
            name='ack',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
