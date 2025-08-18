from django.db import models
from django.contrib.auth.models import User

class QuoteRequest(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    location = models.CharField(max_length=100)  
    submitted_at = models.DateTimeField(auto_now_add=True)



class Todo(models.Model):
    name = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')

    def __str__(self):
        return self.name


    def __str__(self):
        return f"{self.name} - {self.email}"
