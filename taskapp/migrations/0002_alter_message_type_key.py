# Generated by Django 4.1.3 on 2023-01-03 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message_type',
            name='key',
            field=models.IntegerField(unique=True),
        ),
    ]
