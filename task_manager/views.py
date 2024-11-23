from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegisterUserForm, AddTaskForm
from .models import Task
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')
    
    
    
def login_user(request): 
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return render(request, 'login.html', {})
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'You have logged out.')
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered!')
            return redirect('home')
    # If the user haven't submitted (POSTed) data yet,
    # show them the registration form
    else:
        form = RegisterUserForm()
    # If the form is not valid, re-render the form along with
    # user input and error messages.
    return render(request, 'register.html', {'form':form})

@login_required
def add_task(request):
    if request.method == "POST":
        form = AddTaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Task added successfully!")
            return redirect('task_list')
    else:
        form = AddTaskForm()
    return render(request, 'add_task.html', {'form':form})

def update_task(request):
    pass

def delete_task(request):
    pass

def task_list(request):
    pass

@login_required
def task_list(request):
    tasks = Task.objects.all
    return render(request, 'task_list.html')