from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import todo
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
# Create your views here.
@login_required
def home(request):
    if request.method == 'POST':
        task = request.POST.get('task', '').strip()  # Safely get and strip task input
        description = request.POST.get('description', '').strip()  # Safely get description

        if task:  # Ensure task is not empty before saving
            try:
                newtodo = todo(user=request.user, title=task, description=description)
                newtodo.save()
                messages.success(request, 'Task added successfully!')
            except IntegrityError:
                messages.error(request, 'Task with this name already exists.')
        else:
            messages.error(request, 'Task name cannot be empty.')

    alltodo = todo.objects.filter(user=request.user)
    return render(request, 'app/todo.html', {'alltodo': alltodo})

def logoutview(request):
    logout(request)
    return redirect('login') # This will redirect the user to the login page

def register(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 3:
            messages.error(request, 'Password must be at least 3 characters')
            return redirect('register')

        get_all_users_by_username = User.objects.filter(username=username)
        if get_all_users_by_username:
            messages.error(request, 'Error, username already exists, User another.')
            return redirect('register')

        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()

        messages.success(request, 'User successfully created, login now')
        return redirect('login')
    return render(request, 'app/register.html', {})

    
def loginview(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['pass']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')
            return redirect('login')
    return render(request, 'app/login.html')
@login_required
def DeleteTask(request, name):
    try:
        get_todo = todo.objects.get(user=request.user, title=name)  # Use `title`, not `todo_name`
        get_todo.delete()
    except todo.DoesNotExist:
        messages.error(request, "Task does not exist.")
    return redirect('home')

@login_required
def Update(request, name):
    try:
        get_todo = todo.objects.get(user=request.user, title=name)
        get_todo.status = True
        get_todo.save()
    except todo.DoesNotExist:
        messages.error(request, "Task does not exist.")
    return redirect('home')
