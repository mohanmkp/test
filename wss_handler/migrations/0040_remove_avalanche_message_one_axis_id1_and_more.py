# Generated by Django 4.1.3 on 2023-02-10 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wss_handler', '0039_alter_avalanche_message_one_axis_id10_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='axis_id1',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='axis_id10',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='axis_id11',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='axis_id12',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='axis_id13',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='axis_id14',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='axis_id15',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='axis_id2',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='axis_id3',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='axis_id4',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='axis_id5',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='axis_id6',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='axis_id7',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='axis_id8',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='axis_id9',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='forecast_code1',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='forecast_code10',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='forecast_code11',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='forecast_code12',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='forecast_code13',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='forecast_code14',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='forecast_code15',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='forecast_code2',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='forecast_code3',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='forecast_code4',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='forecast_code5',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='forecast_code6',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='forecast_code7',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='forecast_code8',
        ),
        migrations.RemoveField(
            model_name='avalanche_message_one',
            name='forecast_code9',
        ),
        migrations.AddField(
            model_name='avalanche_message_one',
            name='axis_ids',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='avalanche_message_one',
            name='forecast_codes',
            field=models.JSONField(blank=True, null=True),
        ),
    ]