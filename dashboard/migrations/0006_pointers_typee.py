# Generated by Django 4.1.3 on 2023-02-13 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_remove_pointers_point_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='pointers',
            name='typee',
            field=models.CharField(blank=True, choices=[('avalanche', 'avalanche'), ('rain', 'rain')], max_length=200, null=True),
        ),
    ]
