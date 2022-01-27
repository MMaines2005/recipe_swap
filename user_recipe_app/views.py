from distutils.log import error
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import  User, UserManager, Recipe, RecipeManager
import bcrypt

# Create your views here.
def index(request):
    request.session.flush()
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        errors = User.objects.validate_registration(request.POST)
        if len(errors) != 0:
            for key , value in errors.items():
                messages.error(request, value)
            return redirect('/')
        # hash the pw
        hashed_pw = bcrypt.hashpw(
            request.POST['password'].encode(),
            bcrypt.gensalt()
        ).decode()
        # create the user
        new_user = User.objects.create(
            nick_name=request.POST['nick_name'],
            email=request.POST['email'],
            password=hashed_pw,
        )
        request.session['user_id'] = new_user.id
        return redirect('/dashboard')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        errors = User.objects.validate_login(request.POST)
        if len(errors) != 0:
            for key , value in errors.items():
                messages.error(request, value)
                return redirect('/')
        this_user = User.objects.filter(email=request.POST['email'])
        request.session['user_id'] = this_user[0].id
        return redirect('/dashboard')
    return redirect('/')


def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id=request.session['user_id'])

    
    context = {
        'all_recipes': Recipe.objects.all(),
        'user': this_user[0],
        'user_recipes': Recipe.objects.filter(created_by_user=this_user[0]),
    }
    return render(request, 'dashboard.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

# Recipes logic goes here

def update_page(request, recipe_id):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id=request.session['user_id'])
    this_recipe = Recipe.objects.filter(id=recipe_id)
    context = {
        'user': this_user[0],
        'one_recipe': this_recipe[0],
    }
    return render(request, 'update_recipe.html', context)

def add_recipe(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id=request.session['user_id'])

    context = {
        'user': this_user[0]
    }
    
    return render(request, 'add_recipe.html', context)

def create_recipe(request):
    errors = Recipe.objects.validate_recipe(request.POST)
    if len(errors) != 0:
        for value in errors.items():
            messages.error(request, value)
        return redirect('/add_recipe')
    else:
        this_user = User.objects.filter(id=request.session['user_id'])
        recipe = Recipe.objects.create(
            recipe_name = request.POST['recipe_name'],
            recipe_ingredients= request.POST['recipe_ingredients'],
            recipe_instructions= request.POST['recipe_instructions'],
            recipe_servings = request.POST['recipe_instructions'],
            recipe_cook_time = request.POST['recipe_instructions'],
            created_by_user = this_user[0],
            )
    
    return redirect(f'/recipe_detail/{recipe.id}')

def recipe_detail(request, recipe_id):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id=request.session['user_id'])
    this_recipe = Recipe.objects.filter(id=recipe_id)
    context = {
        'user': this_user[0],
        'one_recipe': this_recipe[0],
    }
    return render(request, 'show_one.html', context)

def update_recipe(request, recipe_id):
    recipe_to_update = Recipe.objects.get(id=recipe_id)
    if recipe_to_update.created_by_user.id != request.session['user_id']:
        messages.error(request, "This isn't yours to update.")
        redirect('/edit_page/{{recipe_id}}')
    else:
        recipe_to_update.recipe_name = request.POST['recipe_name']
        recipe_to_update.recipe_ingredients = request.POST['recipe_ingredients']
        recipe_to_update.recipe_instructions = request.POST['recipe_instructions']
        recipe_to_update.recipe_servings = request.POST['recipe_servings']
        recipe_to_update.recipe_cook_time = request.POST['recipe_cook_time']
        recipe_to_update.save()

    return redirect('/dashboard')


def delete_recipe(request, recipe_id):
    recipe_to_delete = Recipe.objects.get(id=recipe_id)
    if recipe_to_delete.created_by_user.id == request.session['user_id']:
        recipe_to_delete.delete()
    else:
        messages.error(request, "This isn't yours to delete.")
    
    return redirect('/dashboard')