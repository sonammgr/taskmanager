from rest_framework import serializers
from .models import Tasks

class Tasksserializers(serializers.ModelSerializer):
    class Meta:
        model=Tasks
        fields='__all__'
        