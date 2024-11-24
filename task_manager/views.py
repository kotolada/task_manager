from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegisterUserForm, AddTaskForm
from .models import Task
from django.contrib.auth.decorators import login_required
from django.utils import timezone


def home(request):
    total_active = Task.objects.filter(user=request.user, task_status=Task.Status.IN_PROGRESS).count()
    total_completed = Task.objects.filter(user=request.user, task_status=Task.Status.DONE).count()
    return render(request, 'home.html', {'total_active': total_active, 'total_completed': total_completed})
    
    
    
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
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, "Task added successfully!")
            return redirect('task_list')
    else:
        form = AddTaskForm()
    return render(request, 'add_task.html', {'form':form})

def edit_task(request, pk):
    if request.user.is_authenticated:
        current_task = Task.objects.get(id=pk)
        # Add instance to propagate the form with
        # the existing information.
        form = AddTaskForm(request.POST or None, instance=current_task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task has been updated.')
            return redirect('task_list')
        return render(request, "edit_task.html", {'form': form})
    else:
        messages.error('You must be logged in to do that.')
        return redirect('login')

def delete_task(request, pk):
    if request.user.is_authenticated:
        delete_it = Task.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Task has been deleted.")
        return redirect('task_list')
    else:
        messages.error('You must be logged in to do that.')
        return redirect('login')

@login_required
def task_list(request): 
    if request.method == "POST":
        task_id = request.POST.get('id')
        try:
            task = Task.objects.get(id=task_id, user=request.user)  # Filter by user
            task.task_status = Task.Status.DONE  # Mark as Done
            task.save()
            messages.success(request, f"Task '{task.task_name}' marked as Done!")
        except Task.DoesNotExist:
            messages.error(request, "Task not found or you don't have permission to update it.")
        return redirect('task_list')
    
    now = timezone.now()        
    tasks = Task.objects.filter(user=request.user, task_status=Task.Status.IN_PROGRESS)
    tasks = tasks.order_by('due_date')
    return render(request, 'task_list.html', {'tasks': tasks, 'now': now})

@login_required
def completed_tasks(request):
    if request.method == "POST":
        task_id = request.POST.get('id')
        try:
            task = Task.objects.get(id=task_id, user=request.user)  # Filter by user
            task.task_status = Task.Status.IN_PROGRESS  # Mark as Done
            task.save()
            messages.success(request, f"Task '{task.task_name}' moved back to the active list!")
        except Task.DoesNotExist:
            messages.error(request, "Task not found or you don't have permission to update it.")
        return redirect('task_list')
    
    tasks = Task.objects.filter(user=request.user, task_status=Task.Status.DONE)
    tasks = tasks.order_by('-due_date')
    return render(request, 'completed_tasks.html', {'tasks': tasks})