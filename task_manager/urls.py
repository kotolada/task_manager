from django.urls import path
from . import views
from .views import ChangePasswordView

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('add_task/', views.add_task, name='add_task'),
    path('task_list/', views.task_list, name='task_list'),
    path('edit_task/<int:pk>', views.edit_task, name='edit_task'),
    path('delete_task/<int:pk>', views.delete_task, name='delete_task'),
    path('completed_tasks/', views.completed_tasks, name='completed_tasks'),
    path('update_user/', views.update_user, name='update_user'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
]