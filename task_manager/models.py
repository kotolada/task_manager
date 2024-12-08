from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):

    class Status(models.TextChoices):
        IN_PROGRESS = 'IN_PROGRESS', _('In Progress')
        DONE = 'DONE', _('Done')
    
    class Priority(models.TextChoices):
        LOW = 'LOW', _('Low')
        MEDIUM = 'MEDIUM', _('Medium')
        HIGH = 'HIGH', _('High')
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=100)
    task_description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    task_status = models.CharField(
        max_length=20,
        choices=Status,
        default=Status.IN_PROGRESS
        )
    task_priority = models.CharField(
        max_length=20,
        choices = Priority,
        default = Priority.LOW
    )
    
    def __str__(self):
        return self.task_name
    