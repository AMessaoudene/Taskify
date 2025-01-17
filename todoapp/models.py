from datetime import date
from django.contrib.auth.models import AbstractUser,User
from django.contrib.auth import get_user_model
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

class todo(models.Model):
    TASK_TYPES = [
        ('études', 'Études'),
        ('travail', 'Travail'),
        ('sport', 'Sport'),
        ('loisirs', 'Loisirs'),
    ]
    TASK_PRIORITIES = [
        ('Élevé', 'élevé Priorité'),
        ('Moyen', 'moyen Priorité'),
        ('Faible', 'Faible Priorité'),
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    todo_name = models.CharField(max_length=1000)
    status = models.BooleanField(default=False)
    due_date = models.DateTimeField(null=True, blank=True)
    task_type = models.CharField(max_length=10, choices=TASK_TYPES)
    task_priority = models.CharField(max_length=10, choices=TASK_PRIORITIES, default='Faible')
    is_deleted = models.BooleanField(default=False)  # Field to mark as deleted instead of directly deleting
    
    def __str__(self):
        return self.todo_name

class Contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=40)
    message = models.TextField(max_length=300)
    def __str__(self):
        return self.name