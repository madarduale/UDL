# Generated by Django 5.0.4 on 2024-07-25 15:14

import embed_video.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('udl_app', '0028_alter_lecture_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='video',
            field=embed_video.fields.EmbedVideoField(blank=True, null=True),
        ),
    ]
