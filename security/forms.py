from django import forms
from .models import Project, ProjectAlotted

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date']

class ProjectAlottedForm(forms.ModelForm):
    class Meta:
        model = ProjectAlotted
        fields = ['manager', 'project', 'employee']