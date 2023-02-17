# Generated by Django 4.1.3 on 2023-01-29 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wss_handler', '0032_receive_message_packet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message_backup',
            name='file',
        ),
        migrations.AddField(
            model_name='message_backup',
            name='file_path',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]