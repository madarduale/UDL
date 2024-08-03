# Generated by Django 5.0.4 on 2024-07-27 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('udl_app', '0031_lecture_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='time',
            field=models.FloatField(blank=True, default=0, help_text='Time in minutes eg. 1.5, 2, 2.1, 3.9', null=True),
        ),
    ]