from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/',views.home, name='home-page'),
    path('register/', views.register, name='register'),
    path('login/', views.loginpage, name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('mark_as_done/<int:task_id>/', views.mark_as_done, name='mark_as_done'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('contact/',views.contact, name='contact'),
    path('restore/<int:task_id>/', views.restore_task, name='restore_task'),
    path('permanent_delete/<int:task_id>/', views.permanent_delete_task, name='permanent_delete_task'),
    path('task_statistics/', views.task_statistics, name='task_statistics'),
]
