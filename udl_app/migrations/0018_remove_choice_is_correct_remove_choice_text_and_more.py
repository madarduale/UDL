# Generated by Django 5.0.4 on 2024-07-10 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('udl_app', '0017_exam_exam_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='is_correct',
        ),
        migrations.RemoveField(
            model_name='choice',
            name='text',
        ),
        migrations.AddField(
            model_name='choice',
            name='correct_text',
            field=models.CharField(choices=[('text1', 'Text 1'), ('text2', 'Text 2'), ('text3', 'Text 3'), ('text4', 'Text 4')], default='text1', max_length=5),
        ),
        migrations.AddField(
            model_name='choice',
            name='text1',
            field=models.CharField(blank=True, default='True', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='choice',
            name='text2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='choice',
            name='text3',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='choice',
            name='text4',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
