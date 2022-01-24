# Generated by Django 3.2.11 on 2022-01-20 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_recipe_app', '0002_recipe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
        migrations.AddField(
            model_name='user',
            name='liked_recipes',
            field=models.ManyToManyField(related_name='liked_recipes', to='user_recipe_app.Recipe'),
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('amount', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ingredients', models.ManyToManyField(related_name='ingredients', to='user_recipe_app.Recipe')),
            ],
        ),
    ]
