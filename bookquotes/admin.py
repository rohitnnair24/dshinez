from django.contrib import admin
from .models import QuoteRequest

@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'location', 'submitted_at') 
    search_fields = ('name', 'email', 'phone_number', 'location') 
    ordering = ('-submitted_at',)
