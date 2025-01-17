from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.db.models import Q
from .models import todo,UserProfile,Contact
from django.db import models
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,FileResponse,JsonResponse
from datetime import date, datetime
from django.urls import reverse

def index(request):
    # Get the current user
    current_user = request.user
    
    # Get uncompleted tasks due today, ordered by priority
    today = date.today()
    uncompleted_tasks_today = todo.objects.filter(user=current_user, due_date__date=today,status=False).order_by('task_priority')
    
    return render(request, 'todoapp/home.html', {'tasks_today': uncompleted_tasks_today})

@login_required
def home(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        user_birthdate = user_profile.date_of_birth.strftime('%Y-%m-%d') if user_profile.date_of_birth else None
    except UserProfile.DoesNotExist:
        user_birthdate = None
    if request.method == 'POST':
        task = request.POST.get('task')
        due_date_str = request.POST.get('due_date')
        due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M').replace(tzinfo=None) if due_date_str else None
        task_type = request.POST.get('task_type')
        task_priority = request.POST.get('task_Priority')
        new_todo = todo(user=request.user, todo_name=task, due_date=due_date, task_type=task_type, task_priority=task_priority, status=False)
        new_todo.save()
        # Redirect after adding the task to avoid resubmission on page refresh
        return redirect('home-page')

    # Fetching tasks
    high_priority_tasks = todo.objects.filter(user=request.user, task_priority='High')
    medium_priority_tasks = todo.objects.filter(user=request.user, task_priority='Medium')
    less_priority_tasks = todo.objects.filter(user=request.user, task_priority='Less')
    deleted_tasks = todo.objects.filter(user=request.user, is_deleted=True)

    # Statistics data
    current_user = request.user
    total_tasks = todo.objects.filter(user=current_user).count()
    total_completed_tasks = todo.objects.filter(user=current_user, status=True).count()
    tasks_by_type = todo.objects.filter(user=current_user, status=True).values('task_type').annotate(count=Count('id'))
    tasks_by_priority = todo.objects.filter(user=current_user, status=True).values('task_priority').annotate(count=Count('id'))

    # Calculating completed task percentages by type
    total_tasks_by_type = todo.objects.filter(user=current_user).values('task_type').annotate(total=Count('id'))
    completed_tasks_by_type = todo.objects.filter(user=current_user, status=True).values('task_type').annotate(completed=Count('id'))
    percentage_by_type = {}
    for task_type in total_tasks_by_type:
        total = task_type['total']
        completed = next((item['completed'] for item in completed_tasks_by_type if item['task_type'] == task_type['task_type']), 0)
        percentage = (completed / total) * 100 if total != 0 else 0
        percentage_by_type[task_type['task_type']] = round(percentage, 2)

    # Calculating completed task percentages by priority
    total_tasks_by_priority = todo.objects.filter(user=current_user).values('task_priority').annotate(total=Count('id'))
    completed_tasks_by_priority = todo.objects.filter(user=current_user, status=True).values('task_priority').annotate(completed=Count('id'))
    percentage_by_priority = {}
    for task_priority in total_tasks_by_priority:
        total = task_priority['total']
        completed = next((item['completed'] for item in completed_tasks_by_priority if item['task_priority'] == task_priority['task_priority']), 0)
        percentage = (completed / total) * 100 if total != 0 else 0
        percentage_by_priority[task_priority['task_priority']] = round(percentage, 2)

    # Context for todo.html template
    context = {
        'user_birthdate': user_profile.date_of_birth,
        'high_priority_tasks': high_priority_tasks,
        'medium_priority_tasks': medium_priority_tasks,
        'less_priority_tasks': less_priority_tasks,
        'deleted_tasks': deleted_tasks,
        'total_tasks': total_tasks,
        'total_completed_tasks': total_completed_tasks,
        'tasks_by_type': tasks_by_type,
        'tasks_by_priority': tasks_by_priority,
        'percentage_by_type': percentage_by_type,
        'percentage_by_priority': percentage_by_priority,
    }
    return render(request, 'todoapp/todo.html', context)

@login_required
def mark_as_done(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(todo, id=task_id, user=request.user)
        task.status = True
        task.save()

    return redirect('home-page')

@login_required
def edit_task(request, task_id):
    if request.method == 'POST':
        updated_task_name = request.POST.get('updated_task_name')
        task = get_object_or_404(todo, id=task_id, user=request.user)
        task.todo_name = updated_task_name
        task.save()
        return redirect('home-page')  # Redirect to the home page after editing the task

    return redirect('home-page')  # Redirect to the home page if not a POST request

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        dob_str = request.POST.get('date_of_birth')

        # Create a new User instance
        new_user = User.objects.create_user(username=username, email=email, password=password)

        # Create a corresponding UserProfile instance
        profile = UserProfile(user=new_user, date_of_birth=dob_str)
        profile.save()

        # Redirect or render success message
        return redirect('login')  # Redirect to login page after successful registration

    return render(request, 'todoapp/register.html')

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home-page')

    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('home-page')
        else:
            messages.error(request, 'Error, wrong user details or user does not exist')
            return render(request,'todoapp/login.html')
    return render(request, 'todoapp/login.html')

@login_required
def delete_task(request, task_id):
    task_to_delete = get_object_or_404(todo, id=task_id, user=request.user)
    if request.method == 'POST':
        # Instead of directly deleting, mark the task as deleted
        if not task_to_delete.is_deleted:
            task_to_delete.is_deleted = True
            task_to_delete.save()
            return redirect('home-page')

    return render(request, 'todoapp/todo.html')

@login_required
def restore_task(request, task_id):
    task_to_restore = get_object_or_404(todo, id=task_id, user=request.user, is_deleted=True)
    
    if request.method == 'POST':
        task_to_restore.is_deleted = False
        task_to_restore.save()
        return redirect('home-page')  # Redirect to the home page after restoring the task

    return redirect('home-page')  # Redirect to the home page if the method is not POST

@login_required
def permanent_delete_task(request, task_id):
    task_to_delete_permanently = get_object_or_404(todo, id=task_id, user=request.user, is_deleted=True)
    
    if request.method == 'POST':
        task_to_delete_permanently.delete()
        return redirect('home-page')  # Redirect to the home page after permanently deleting the task

    return redirect('home-page')  # Redirect to the home page if the method is not POST

def loginfail(request):
    return render(request, 'todoapp/register.html', {})

def logout_view(request):
    logout(request)
    return redirect(reverse('login'))

def contact(request):
    if request.method=="POST":
        contact= Contact()
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')
        contact.name=name
        contact.email=email
        contact.message=message
        contact.save()
    return render(request,'todoapp/contact.html')

from django.db.models import Count

@login_required
def task_statistics(request):
    # Get the current user
    current_user = request.user
    
    # General Statistics
    total_completed_tasks = todo.objects.filter(user=current_user, status=True).count()
    
    # By Type Statistics
    tasks_by_type = todo.objects.filter(user=current_user, status=True).values('task_type').annotate(count=Count('id'))
    
    # By Priority Statistics
    tasks_by_priority = todo.objects.filter(user=current_user, status=True).values('task_priority').annotate(count=Count('id'))

    # Calculating completed task percentages by type
    total_tasks_by_type = todo.objects.filter(user=current_user).values('task_type').annotate(total=Count('id'))
    completed_tasks_by_type = todo.objects.filter(user=current_user, status=True).values('task_type').annotate(completed=Count('id'))

    percentage_by_type = {}
    for task_type in total_tasks_by_type:
        total = task_type['total']
        completed = next((item['completed'] for item in completed_tasks_by_type if item['task_type'] == task_type['task_type']), 0)
        percentage = (completed / total) * 100 if total != 0 else 0
        percentage_by_type[task_type['task_type']] = round(percentage, 2)

    # Calculating completed task percentages by priority
    total_tasks_by_priority = todo.objects.filter(user=current_user).values('task_priority').annotate(total=Count('id'))
    completed_tasks_by_priority = todo.objects.filter(user=current_user, status=True).values('task_priority').annotate(completed=Count('id'))

    percentage_by_priority = {}
    for task_priority in total_tasks_by_priority:
        total = task_priority['total']
        completed = next((item['completed'] for item in completed_tasks_by_priority if item['task_priority'] == task_priority['task_priority']), 0)
        percentage = (completed / total) * 100 if total != 0 else 0
        percentage_by_priority[task_priority['task_priority']] = round(percentage, 2)
    
    return render(request, 'todoapp/statistics.html', {
        'total_completed_tasks': total_completed_tasks,
        'tasks_by_type': tasks_by_type,
        'tasks_by_priority': tasks_by_priority,
        'percentage_by_type': percentage_by_type,
        'percentage_by_priority': percentage_by_priority,
    })