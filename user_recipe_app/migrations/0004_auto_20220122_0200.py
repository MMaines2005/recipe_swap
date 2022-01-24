# Generated by Django 3.2.11 on 2022-01-22 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_recipe_app', '0003_auto_20220120_1429'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='image',
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Ingredient',
        ),
    ]