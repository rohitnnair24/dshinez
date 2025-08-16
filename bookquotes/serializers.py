from rest_framework import serializers
from .models import QuoteRequest

class QuoteRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteRequest
        fields = ['id', 'name', 'phone_number', 'email', 'location', 'submitted_at']
