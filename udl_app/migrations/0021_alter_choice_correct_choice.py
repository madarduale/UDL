# Generated by Django 5.0.4 on 2024-07-10 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('udl_app', '0020_rename_choice1_choice_choice_remove_choice_choice2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='correct_choice',
            field=models.CharField(blank=True, default='False', max_length=7, null=True),
        ),
    ]
