# Generated by Django 4.1.3 on 2023-01-06 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wss_handler', '0005_alter_hourly_data_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hourly_data',
            name='aws_time',
            field=models.CharField(max_length=4),
        ),
    ]
