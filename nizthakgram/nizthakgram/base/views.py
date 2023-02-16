from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth 
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'index.html')


@login_required(login_url='signin')
def settings(request):
    return render(request, 'settings.html')

@login_required(login_url='signin')
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'email is already taken!')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'username already taken!')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()


                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user = user_model, id_user = user.id)
                new_profile.save()
                return redirect('signup')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('signup')
    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid login details')
            return redirect('signin')
    return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):

    return redirect('signin')