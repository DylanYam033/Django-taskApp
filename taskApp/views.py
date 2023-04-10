from django.shortcuts import render, redirect, get_object_or_404
# crear y autenticar usuarios
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
# crea una cookie de autenticacion
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
# importamos el formulario para pasarlo el template de create.html
from .forms import CreateTask
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')


def singup(request):

    if request.method == 'GET':
        return render(request, 'singup.html', {
            'form': UserCreationForm
        })

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'singup.html', {
                    'form': UserCreationForm,
                    'error': "user already exist"
                })
        else:
            return render(request, 'singup.html', {
                'form': UserCreationForm,
                'error': "password invalid"
            })

@login_required
def tasks(request):
    # traemos solo las tareas del usuario en sesion
    tasks = Task.objects.filter(user=request.user, dateCompleted__isnull=True)
    if tasks.exists():
        # Si hay tareas, las mostramos
        return render(request, 'tasks.html', {
            'tasks': tasks
        })
    else:
        # Si no hay tareas, mostramos un mensaje
        message = "No hay tareas aún"
        return render(request, 'tasks.html', {
            'message': message
        })

@login_required   
def tasksCompleted(request):
    # traemos solo las tareas del usuario en sesion
    tasks = Task.objects.filter(user=request.user, dateCompleted__isnull=False).order_by('-dateCompleted')
    if tasks.exists():
        # Si hay tareas, las mostramos
        return render(request, 'tasks/completed.html', {
            'tasks': tasks
        })
    else:
        # Si no hay tareas, mostramos un mensaje
        message = "No hay tareas completadas"
        return render(request, 'tasks/completed.html', {
            'message': message
        })

@login_required
def log_out(request):
    logout(request)
    return redirect('home')


def singin(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        print(request.POST)
        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': "username or password is incorrect"
            })
        else:
            # guardamos la sesion del usuario con la cookie
            login(request, user)
            return redirect('home')

@login_required
def createTask(request):
    if request.method == 'GET':
        return render(request, 'tasks/create.html', {
            'createForm': CreateTask
        })
    else:
        try:
            data = CreateTask(request.POST)
            new_task = data.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'tasks/create.html', {
                'createForm': CreateTask,
                'error': 'Datos invalidos'
            })

@login_required
def taskDetail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user) 
        form = CreateTask(instance=task)
        return render(request,'tasks/detail.html',{
            'task': task,
            'form': form
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            newForm = CreateTask(request.POST, instance=task)
            newForm.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'tasks/detail.html',{
            'task': task,
            'form': form,
            'error': "No se pudo editar la tarea"
        })

@login_required
def completeTask(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user )
    if request.method == 'POST':
        task.dateCompleted = timezone.now()
        task.save()
        return redirect('tasks')
    
@login_required
def deleteTask(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user )
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
