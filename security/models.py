from django.db import models
from django.contrib.auth.models import User
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
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee')
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_employee_active = models.BooleanField(default=False)
    def __str__(self):
        return self.project.name + ' - ' + self.employee.user.username
    
    def get_manager(self):
        return self.manager.user.username


       


