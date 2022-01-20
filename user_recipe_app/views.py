from django.shortcuts import render, redirect
from django.contrib import messages
from user_recipe_app.models import  User, UserManager
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        errors = User.objects.validate_registration(request.POST)
        if len(errors) != 0:
            for key , value in errors.items():
                messages.error(request, value)
                return redirect('/')
        this_user = User.objects.create(
            nick_name=request.POST['nick_name'],
            email=request.POST['email'],
            password=request.POST['password'],
        )
        request.session['user_id'] = this_user
        return redirect('/success')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        errors = User.objects.validate_login(request.POST)
        if len(errors) != 0:
            for key , value in errors.items():
                messages.error(request, value)
                return redirect('/')
        this_user = User.objects.filter(email=request.POST['email'])
        request.session['user_id'] = this_user
        return redirect('/success')
    return redirect('/')


def success(request):
    return render(request, 'dashboard.html')

def logout(request):
    request.session.clear()
    return redirect('/')
