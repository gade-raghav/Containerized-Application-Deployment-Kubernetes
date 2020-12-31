from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import *
from .forms import *
from .decorators import *




#--Error Pages
def error_500_view(request):
    return render(request,'500.html')

def error_404_view(request,exception):
    return render(request,'404.html')


#--Signin/Signout--#
#--Signin
@unauthenticated_user
def signin(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
            
        if user is not None:
            login(request,user)
            messages.info(request, 'Logged in successfully!')
            return redirect('home')
        else:
            messages.error(request,'username or password not correct')
            return redirect('signin')
    
    context = {
            'form': form
    }

    return render(request,'employees/signin.html',context)


#--Signout
def signout(request):
    logout(request)
    messages.info(request, 'Logged out.')
    return redirect('home')

#--Home-Page--#
def home(request):
    employees = Employee.objects.all()
    context = {'employees':employees}
    return render(request, 'employees/home.html',context)

#--Employee--#
#--Add-Employee
@login_required(login_url='signin')
def addEmployee(request):
    form = EmployeeForm()
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Updated.')
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'employees/add.html',context)

