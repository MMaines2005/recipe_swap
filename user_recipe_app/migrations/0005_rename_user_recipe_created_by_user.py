# Generated by Django 3.2.11 on 2022-01-22 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_recipe_app', '0004_auto_20220122_0200'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='user',
            new_name='created_by_user',
        ),
    ]
