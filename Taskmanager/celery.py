import os 
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Taskmanager.settings')
app = Celery('Taskmanager')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()