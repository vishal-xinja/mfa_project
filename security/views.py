from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectAlotted
from .forms import ProjectForm, ProjectAlottedForm
from django.contrib import messages

# Create your views here.
def manager_dashboard(request):
    return render(request, 'manager/dashboard.html')

def employee_dashboard(request):
    return render(request, 'employee/dashboard.html')

def add_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project added successfully.')
        else:
            messages.error(request, 'Error adding project.')
    return redirect('mdashboard')

def project_details(request, pk):   
    project= Project.objects.get(pk=pk)
    project_alotted = ProjectAlotted.objects.filter(project=project)
    return render(request, 'project/project_details.html', {'project': project, 'project_alotted': project_alotted})