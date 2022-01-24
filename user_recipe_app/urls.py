from django.urls import path
from . import views

urlpatterns = [
    # User management urls
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('dashboard', views.success, name='success'),
    path('logout', views.logout, name='logout'),
    # Recipes urls
    path('add_recipe', views.add_recipe, name='add_recipe'),
    path('create_recipe', views.create_recipe, name='create_recipe'),
    path('recipe_detail/<int:recipe_id>', views.recipe_detail, name='recipe_detail'),

]