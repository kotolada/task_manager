from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegisterUserForm, UpdateUserForm, AddTaskForm
from .models import Task
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.postgres.search import SearchVector
from django.db.models import Case, When, Value, IntegerField
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin


def home(request):
    if request.user.is_authenticated is False:
        return render(request, 'home.html', {})

    total_active = Task.objects.filter(
        user=request.user, task_status=Task.Status.IN_PROGRESS).count()
    total_completed = Task.objects.filter(
        user=request.user, task_status=Task.Status.DONE).count()

    return render(request, 'home.html', {'total_active': total_active, 'total_completed': total_completed})


def login_user(request):
    if request.method != 'POST':
        return render(request, 'login.html')

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is None:
        messages.error(
            request, "Invalid username or password. Please try again.")
        return render(request, 'login.html', {})

    login(request, user)
    messages.success(request, "You have been logged in!")
    return redirect('home')


def logout_user(request):
    logout(request)
    messages.success(request, 'You have logged out.')
    return redirect('home')


def register_user(request):
    if request.method != 'POST':
        return render(request, 'register.html', {'form': RegisterUserForm()})

    form = RegisterUserForm(request.POST)

    if form.is_valid() is False:
        return render(request, 'register.html', {'form': form})

    form.save()
    messages.success(request, 'You have successfully registered!')

    return redirect('login')


@login_required
def update_user(request):
    if request.method == "POST":
        form = UpdateUserForm(request.POST, instance=request.user)

        if form.is_valid() is False:
            return render(request, 'update_user.html', {'form': form})

        form.save()
        messages.success(request, 'Your profile has been updated!')
        return redirect('update_user')

    form = UpdateUserForm(instance=request.user)

    return render(request, 'update_user.html', {'form': form})


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = "Password changed successfully."
    success_url = reverse_lazy('home')


@login_required
def add_task(request):
    if request.method != 'POST':
        return render(request, 'add_task.html', {'form': AddTaskForm()})

    form = AddTaskForm(request.POST)

    if form.is_valid() == False:
        return render(request, 'add_task.html', {'form': form})

    task = form.save(commit=False)
    task.user = request.user
    task.save()

    messages.success(request, "Task added successfully!")

    return redirect('task_list')


@login_required
def edit_task(request, pk):
    current_task = get_object_or_404(Task, id=pk)
    task_name = current_task.task_name

    # Add instance to propagate the form with the existing information.
    form = AddTaskForm(request.POST or None, instance=current_task)

    if form.is_valid() is False:
        return render(request, "edit_task.html", {'form': form})

    form.save()
    messages.success(request, f'Task "{task_name}" has been updated.')
    return redirect('task_list')


@login_required
def delete_task(request, pk):
    delete_it = get_object_or_404(Task, id=pk)
    delete_it.delete()
    task_name = delete_it.task_name

    messages.success(request, f'Task "{task_name}" has been deleted.')
    return redirect('task_list')


@login_required
def task_list(request):
    tasks = Task.objects.filter(
        user=request.user, task_status=Task.Status.IN_PROGRESS).order_by('due_date')

    # Adding search functionality
    query = request.GET.get('q', '')
    if query:
        tasks = Task.objects.annotate(
            # Search in both name and desc
            search=SearchVector('task_name', 'task_description')
        ).filter(search=query, user=request.user, task_status=Task.Status.IN_PROGRESS)

    # Adding sorting functionality
    priority_order = Case(
        When(task_priority='LOW', then=Value(1)),
        When(task_priority='MEDIUM', then=Value(2)),
        When(task_priority='HIGH', then=Value(3)),
        output_field=IntegerField(),
    )
    tasks = tasks.annotate(priority_order=priority_order)
    sort = request.GET.get('sort')
    if sort == 'task_priority':
        tasks = tasks.order_by('priority_order')
    elif sort == '-task_priority':
        tasks = tasks.order_by('-priority_order')

    # Adding the 'DONE' button to update the task status in the db
    if request.method == "POST":
        task_id = request.POST.get('id')

        task = get_object_or_404(Task,
                                 id=task_id, user=request.user)  # Filter by user
        task.task_status = Task.Status.DONE  # Mark as Done
        task.save()
        
        messages.success(request, f'Task "{
            task.task_name}" marked as Done!')
        return redirect('task_list')

    # Adding a timezone variable to enable comparison in the template
    now = timezone.now()
    # tasks = tasks.order_by('due_date')
    return render(request, 'task_list.html', {'tasks': tasks, 'now': now, 'query': query, 'sort': sort})


@login_required
def completed_tasks(request):
    tasks = Task.objects.filter(
        user=request.user, task_status=Task.Status.DONE)

    # Adding search functionality
    query = request.GET.get('q', '')
    if query:
        tasks = Task.objects.annotate(
            # Search in both name and desc
            search=SearchVector('task_name', 'task_description')
        ).filter(search=query, user=request.user, task_status=Task.Status.DONE)

    if request.method == "POST":
        task_id = request.POST.get('id')
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.task_status = Task.Status.IN_PROGRESS
        task.save()
        
        messages.success(request, f'Task "{
                         task.task_name}" moved back to the active list!')

        return redirect('task_list')

    tasks = tasks.order_by('-due_date')
    return render(request, 'completed_tasks.html', {'tasks': tasks, 'query': query})
