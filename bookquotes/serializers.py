from .models import QuoteRequest
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Todo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'name', 'completed']


class QuoteRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteRequest
        fields = ['id', 'name', 'phone_number', 'email', 'location', 'submitted_at']
