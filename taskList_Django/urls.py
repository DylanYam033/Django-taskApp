from django.contrib import admin
from django.urls import path
from taskApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('singup/', views.singup, name='singup'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks_completed/', views.tasksCompleted, name='tasksCompleted'),
    path('logout/', views.log_out, name='logout'),
    path('login/', views.singin, name='login'),
    path('createTask/', views.createTask, name='createTask'),
    path('tasks/<int:task_id>/', views.taskDetail, name='detailTask'),
    path('tasks/<int:task_id>/completed', views.completeTask, name='completeTask'),
    path('tasks/<int:task_id>/deleted', views.deleteTask, name='deleteTask'),
]

