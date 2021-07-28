from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, CustomerForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages
from .models import *
# Create your views here.


def RegisterView(request):
    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password1'],)
            login(request,new_user)
            return redirect(reverse('setup'))

    context = {'form': form}
    return render(request, 'baseapp/register.html', context)

def LoginView(request):
    context = {}
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('Username'),password=request.POST.get('Password'))
        
        if user is not None:
            login(request, user)
            return redirect(reverse('home'))
        else:
            messages.info(request, 'Username or Password is incorrect.')

    return render(request, 'baseapp/login.html', context)

def LogoutView(request):
    logout(request)
    return redirect(reverse('login'))

def SetUp(request):
    if request.user.is_authenticated:
        form = CustomerForm()
        context = {'form':form}

        if request.method == 'POST':
            #print(request.POST)
            form = CustomerForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()
            return redirect(reverse('home'))

        return render(request, 'baseapp/accountsetup.html', context)
    else:
        return redirect(reverse('home'))

def empty(request):
    return redirect('home/')

def home(request):
    if request.user.is_authenticated:
        try:
            u = Customer.objects.get(user=request.user)
        except:
            return render(request, 'baseapp/index.html')
        return render(request, 'baseapp/index.html', {'u':u})

    return render(request, 'baseapp/index.html')