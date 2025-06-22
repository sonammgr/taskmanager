
from django.urls import path
from .views import PublictaskView, MyTasksViewSet, register

urlpatterns = [
    path('public-tasks/', PublictaskView.as_view(), name='public-task-list'),
    path('my-tasks/', MyTasksViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='my-tasks-list-create'),
    path('my-tasks/<int:pk>/', MyTasksViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='my-tasks-detail'),
    path('register/', register, name='register'),
]