from django.shortcuts import render
from .models import Tasks
from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import Tasksserializers
from django.http import HttpResponse
from .tasks import send_welcome_email


class PublictaskView(ListAPIView):
    permission_classes=[AllowAny]
    queryset=Tasks.objects.filter(is_public=True)
    serializer_class=Tasksserializers


class MyTasksViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=Tasksserializers

    def get_queryset(self):
        return Tasks.objects.filter(assignee=self.request.user)

def register(request):
    user_email="user@example.com"
    send_welcome_email.delay(user_email)
    return HttpResponse("REGUSTRATION SUCCESSFULL, EMAIL QUEUD")