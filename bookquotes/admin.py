from django.contrib import admin
from .models import QuoteRequest
from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'completed', 'owner')
    list_filter = ('completed',)
    search_fields = ('name', 'owner__username')


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'location', 'submitted_at') 
    search_fields = ('name', 'email', 'phone_number', 'location') 
    ordering = ('-submitted_at',)
