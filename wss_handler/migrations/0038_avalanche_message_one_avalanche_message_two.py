# Generated by Django 4.1.3 on 2023-02-08 06:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wss_handler', '0037_site_critical_alert'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avalanche_message_one',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='avalanche_files/')),
                ('ack', models.BooleanField(blank=True, null=True)),
                ('sequence_num', models.IntegerField()),
                ('message_on', models.DateTimeField(auto_now_add=True)),
                ('data', models.JSONField()),
                ('packet', models.CharField(max_length=255)),
                ('message_type', models.IntegerField()),
                ('start_date', models.CharField(max_length=6)),
                ('grid_id', models.CharField(max_length=4)),
                ('num_of_axis', models.IntegerField(verbose_name=range(1, 16))),
                ('axis_id1', models.CharField(max_length=2)),
                ('forecast_code1', models.CharField(max_length=1)),
                ('axis_id2', models.CharField(blank=True, max_length=2, null=True)),
                ('forecast_code2', models.CharField(blank=True, max_length=1, null=True)),
                ('axis_id3', models.CharField(blank=True, max_length=2, null=True)),
                ('forecast_code3', models.CharField(blank=True, max_length=1, null=True)),
                ('axis_id4', models.CharField(blank=True, max_length=2, null=True)),
                ('forecast_code4', models.CharField(blank=True, max_length=1, null=True)),
                ('axis_id5', models.CharField(blank=True, max_length=2, null=True)),
                ('forecast_code5', models.CharField(blank=True, max_length=1, null=True)),
                ('axis_id6', models.CharField(blank=True, max_length=2, null=True)),
                ('forecast_code6', models.CharField(blank=True, max_length=1, null=True)),
                ('axis_id7', models.CharField(blank=True, max_length=2, null=True)),
                ('forecast_code7', models.CharField(blank=True, max_length=1, null=True)),
                ('axis_id8', models.CharField(blank=True, max_length=2, null=True)),
                ('forecast_code8', models.CharField(blank=True, max_length=1, null=True)),
                ('axis_id9', models.CharField(blank=True, max_length=2, null=True)),
                ('forecast_code9', models.CharField(blank=True, max_length=1, null=True)),
                ('axis_id10', models.CharField(blank=True, max_length=2, null=True)),
                ('forecast_code10', models.CharField(blank=True, max_length=1, null=True)),
                ('axis_id11', models.CharField(blank=True, max_length=2, null=True)),
                ('forecast_code11', models.CharField(blank=True, max_length=1, null=True)),
                ('axis_id12', models.CharField(blank=True, max_length=2, null=True)),
                ('forecast_code12', models.CharField(blank=True, max_length=1, null=True)),
                ('axis_id13', models.CharField(blank=True, max_length=2, null=True)),
                ('forecast_code13', models.CharField(blank=True, max_length=1, null=True)),
                ('axis_id14', models.CharField(blank=True, max_length=2, null=True)),
                ('forecast_code14', models.CharField(blank=True, max_length=1, null=True)),
                ('axis_id15', models.CharField(blank=True, max_length=2, null=True)),
                ('forecast_code15', models.CharField(blank=True, max_length=1, null=True)),
                ('sender_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Avalanche_message_two',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_type', models.IntegerField()),
                ('forecast_start_date', models.CharField(max_length=6)),
                ('grid_id', models.CharField(max_length=4)),
                ('outlook', models.CharField(max_length=124)),
                ('avalanche_one', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='wss_handler.avalanche_message_one')),
            ],
        ),
    ]
