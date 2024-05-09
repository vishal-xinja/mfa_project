from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectAlotted,ProjectAuth
from .forms import ProjectForm, ProjectAuthForm
from django.contrib import messages
from django.contrib.auth.models import User, Group
# pagination 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
@login_required
def manager_dashboard(request):
    all_projects = Project.objects.filter(manager=request.user)
    all_project_alloted = ProjectAlotted.objects.filter(manager=request.user)
    all_employees = User.objects.filter(is_employee=True)
    paginator_project = Paginator(all_projects, 5)
    paginator_project_alloted = Paginator(all_project_alloted, 5)
    paginator_employee = Paginator(all_employees, 5)

    page = request.GET.get('prjpage')
    page_alloted = request.GET.get('prjallotedpage')
    page_employee = request.GET.get('emppage')
    try:
        projects = paginator_project.page(page)
        project_alloted = paginator_project_alloted.page(page_alloted)
        employees = paginator_employee.page(page_employee)
    except PageNotAnInteger:
        projects = paginator_project.page(1)
        project_alloted = paginator_project_alloted.page(1)
        employees = paginator_employee.page(1)
    except EmptyPage:
        projects = paginator_project.page(paginator_project.num_pages)
        project_alloted = paginator_project_alloted.page(paginator_project_alloted.num_pages)
        employees = paginator_employee.page(paginator_employee.num_pages)
    print(f'len of projects {len(projects)}')
    ctx = {
        'projects': projects,
        'project_alloted': project_alloted,
        'employees': employees,
    }
    return render(request, 'accounts/manager/dashboard.html', ctx)

@login_required
def employee_dashboard(request):
    return render(request, 'accounts/employee/dashboard.html')

@login_required
def add_project(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        manager = request.user
        if len(name) < 3:
            messages.error(request, 'Project name must be at least 3 characters.')
            return redirect('mdashboard')
        if len(description) < 5:
            messages.error(request, 'Project description must be at least 10 characters.')
            return redirect('mdashboard')
        if not start_date:
            messages.error(request, 'Start date is required.')
            return redirect('mdashboard')
        if not end_date:
            messages.error(request, 'End date is required.')
            return redirect('mdashboard')
        project = Project(name=name, description=description, start_date=start_date, end_date=end_date, manager=manager)
        project.save()
        messages.success(request, 'Project added successfully.')
    return redirect('mdashboard')

@login_required
def project_details(request, pk):   
    project= Project.objects.get(pk=pk)
    members = ProjectAlotted.objects.filter(project=project)
    auth = ProjectAuth.objects.filter(project=project)
    return render(request, 'project_details.html', {'project': project, 'members': members, 'pid': pk, 'auth': auth})

@login_required
def asign_employee_to_project(request, pk):
    project = Project.objects.get(pk=pk)
    # users that belong to group 'employee'
    group = Group.objects.get(name='employee')
    employees = User.objects.filter(groups=group)
    # remove employees that are already assigned to the project
    project_alotted = ProjectAlotted.objects.filter(project=project)
    for p in project_alotted:
        employees = employees.exclude(pk=p.employee.pk)
    if request.method == 'POST':
        emp_id = request.POST.get('emp')
        manager_id = request.POST.get('manager_id')
        project_id = request.POST.get('project_id')
        employee = User.objects.get(pk=emp_id)
        manager = User.objects.get(pk=manager_id)
        project = Project.objects.get(pk=project_id)
        project_alotted = ProjectAlotted(manager=manager, project=project, employee=employee)
        project_alotted.save()
        messages.success(request, 'Employee added to project successfully.')
        return redirect('project_detail', pk=project.pk)

    return render(request, 'assign_e_to_p.html', { 
        'project': project, 
        'employees': employees}
    )

@login_required
def remove_employee_from_project(request, pa):
    project_alotted = ProjectAlotted.objects.get(pk=pa)
    project_alotted.delete()
    messages.success(request, 'Employee removed from project successfully.')
    return redirect('project_details', pk=project_alotted.project.pk)

@login_required
def delete_project(request, pk):
    project = Project.objects.get(pk=pk)
    project.delete()
    messages.success(request, 'Project deleted successfully.')
    return redirect('all_projects')

@login_required
def all_projects(request):
    manager = request.user
    projects = Project.objects.filter(manager=manager)
    return render(request, 'all_projects.html', {'projects': projects})

@login_required
def edit_project(request, pk):
    project = Project.objects.get(pk=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully.')
            return redirect('all_projects')
    return render(request, 'edit_project.html', {'form': form})

@login_required
def set_project_auth(request, pk):
    project = Project.objects.get(pk=pk)
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        defaultSecretSalt = request.POST.get('defaultSecretSalt')
        regenerateTime = request.POST.get('regenerateTime')
        regenerateSchedule = request.POST.get('regenerateSchedule')
        expiryDate = request.POST.get('expiryDate')
        authenticationType = request.POST.get('authenticationType')
        project = Project.objects.get(pk=project_id)
        if not defaultSecretSalt:
            messages.error(request, 'Default secret salt is required.')
            return redirect('set_project_auth', pk=project.pk)
        if not regenerateTime:
            messages.error(request, 'Regenerate time is required.')
            return redirect('set_project_auth', pk=project.pk)
        if not regenerateSchedule:
            messages.error(request, 'Regenerate schedule is required.')
            return redirect('set_project_auth', pk=project.pk)
        if not expiryDate:
            messages.error(request, 'Expiry date is required.')
            return redirect('set_project_auth', pk=project.pk)
        if not authenticationType:
            messages.error(request, 'Authentication type is required.')
            return redirect('set_project_auth', pk=project.pk)
        project_auth = ProjectAuth(project=project, 
                                   expiry_date=expiryDate, 
                                   salt = defaultSecretSalt,
                                   schedule=regenerateSchedule, 
                                   regen_time=regenerateTime)
        project_auth.save()
        messages.success(request, 'Project authentication set successfully.')
        return redirect('project_detail', pk=project.pk)
    return render(request, 'set_project_auth.html', {
        'project': project,
    }) 

@login_required
def edit_project_auth(request, pk):
    project = Project.objects.get(pk=pk)
    auth = ProjectAuth.objects.get(project=project)
    form = ProjectAuthForm(instance=auth)
    if request.method == 'POST':
        form = ProjectAuthForm(request.POST, instance=auth)
        if form.is_valid():
            model = form.save(commit=False)
            model.project= project
            model.save()
            messages.success(request, 'Project authentication updated successfully.')
            return redirect('project_detail', pk=pk)
    return render(request, 'edit_project_auth.html', {
        'form': form,
        'project': project,
    })

@login_required
def employee_project_auth(request, pk):
    return render(request, 'employee_project_auth.html')

@login_required
def employee_project_auth(request, pk):
    return render(request, 'employee_project_auth.html')






