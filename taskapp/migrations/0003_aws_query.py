# Generated by Django 4.1.3 on 2023-01-10 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskapp', '0002_alter_message_type_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='aws_query',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
                ('title', models.CharField(max_length=255)),
            ],
        ),
    ]
