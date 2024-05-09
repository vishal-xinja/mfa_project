from django.contrib import admin
from .models import Project, ProjectAlotted, User, ProjectAuth
# Register your models here.

admin.site.register(Project)
admin.site.register(ProjectAlotted)
admin.site.register(ProjectAuth)

