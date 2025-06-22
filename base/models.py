from django.db import models
from django.contrib.auth.models import User

class Telegramuser(models.Model):
    telegram_username=models.CharField(max_length=100, unique=True)
    telegram_chat_id=models.CharField(max_length=50)
    user=models.OneToOneField(User, on_delete=models.CASCADE)

class Tasks(models.Model):
    PRIORITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]
    STATUS_CHOICES = [('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')]
    
    title=models.CharField(max_length=100)
    description=models.TextField(max_length=300)
    assignee=models.ForeignKey(User, on_delete=models.CASCADE)
    priority=models.CharField(max_length=50, choices=PRIORITY_CHOICES)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES)
    is_public=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)