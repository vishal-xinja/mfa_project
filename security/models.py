from django.db import models
from django.contrib.auth.models import User, Group
# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='Project description')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_manager', default=1)
    
    def __str__(self):
        return self.name
    
    def total_employees(self):
        return self.projectalotted_set.all().count()
    
class ProjectAlotted(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manager')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project')
    # only user that belong to group employee
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee')
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_employee_active = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.project.name} - {self.employee.username}"
    
    def get_manager(self):
        return self.manager.username

class ProjectAuth(models.Model):
    schedule_choices = ('d', 'Daily'), ('w', 'Weekly'), ('m', 'Monthly'), ('y', 'Yearly')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_auth')
    expiry_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    salt = models.CharField(max_length=100, default='salt')
    schedule = models.CharField(max_length=1, choices=schedule_choices, default='d')
    is_active = models.BooleanField(default=True)
    regen_time = models.TimeField(blank=True, null=True)
    
    def __str__(self):
        return self.project.name
    
    def get_all_employees(self):
        return self.projectalotted_set.all()
       


