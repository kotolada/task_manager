from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Task(models.Model):

    class Status(models.TextChoices):
        NEW = 'NEW', _('New')
        IN_PROGRESS = 'IN_PROGRESS', _('In Progress')
        DONE = 'DONE', _('Done')

    task_name = models.CharField(max_length=100)
    task_description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    task_status = models.CharField(
        max_length=20,
        choices=Status,
        default=Status.NEW
        )
    
    def __str__(self):
        return self.task_name