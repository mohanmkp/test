# Generated by Django 4.1.3 on 2023-01-17 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wss_handler', '0020_query_send_message_sequence_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query_send_message',
            name='sequence_num',
            field=models.IntegerField(default=50, unique=True),
        ),
    ]
