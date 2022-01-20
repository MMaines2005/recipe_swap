from django.shortcuts import render, redirect
from django.contrib import messages
from .models import  User, UserManager
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
        'user': this_user[0]
    }
    return render(request, 'dashboard.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')
