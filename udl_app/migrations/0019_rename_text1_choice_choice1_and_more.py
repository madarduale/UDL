# Generated by Django 5.0.4 on 2024-07-10 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('udl_app', '0018_remove_choice_is_correct_remove_choice_text_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='text1',
            new_name='choice1',
        ),
        migrations.RenameField(
            model_name='choice',
            old_name='text2',
            new_name='choice2',
        ),
        migrations.RenameField(
            model_name='choice',
            old_name='text3',
            new_name='choice3',
        ),
        migrations.RenameField(
            model_name='choice',
            old_name='text4',
            new_name='choice4',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='text',
            new_name='question',
        ),
        migrations.RemoveField(
            model_name='choice',
            name='correct_text',
        ),
        migrations.AddField(
            model_name='choice',
            name='correct_choice',
            field=models.CharField(choices=[('choice1', 'choice 1'), ('choice2', 'choice 2'), ('choice3', 'choice 3'), ('choice4', 'choice 4')], default='choice1', max_length=7),
        ),
    ]
