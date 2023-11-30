from django.db import models
from django.contrib.auth.models import User
from django import forms


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        # mostrar los titulos de las tareas
        return self.title + " de " + self.user.username
