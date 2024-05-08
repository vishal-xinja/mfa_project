from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    gender_choices = [
        ('male', "Male"),
        ('female', "Female"),
        ('other', "Dont want to disclose")
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    picture= models.ImageField(upload_to='profile/')
    gender = models.CharField(max_length=10, choices=gender_choices)
    bio = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)

# dashboard/models.py
from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name

