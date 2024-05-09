from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from security.forms import ProjectForm, ProjectAlottedForm
from security.models import Project, ProjectAlotted
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def emp_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # check if user belongs to group employee
            if user.groups.filter(name='employee').exists():
                login(request, user)
            return redirect('emp_dashboard')  # Redirect to the employee dashboard upon successful login
        else:
            return render(request, 'emp_login.html', {'error_message': 'Invalid username or password.'})
    else:
        return render(request, 'accounts/employee/emp_login.html')
    
def emp_logout(request):
    logout(request)
    return redirect('home')  # Redirect to the home page after logout


def emp_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            user =  User.objects.create_user(username=username, password=password)
            group = Group.objects.get(name='employee')
            user.groups.add(group)
            user.save()
            messages.success(request, 'Registered')
            return redirect('emp_login')  # Redirect to the employee login page after successful registration
        else:
            messages.error(request, 'Failed')
            return render(request, 'emp_register.html', {'error_message': 'Passwords do not match.'})
    else:
        return render(request, 'accounts/employee/emp_register.html')

def man_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # check if user belongs to group manager
            if user.groups.filter(name='manager').exists():
                login(request, user)
                messages.success(request, 'You have successfully logged in.')
                return redirect('mdashboard')  # Redirect to the employee dashboard upon successful login
            else:
                messages.error(request, 'You are not authorized to access this page.')
                return redirect('man_login')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/manager/login.html')
    
@login_required
def mdashboard(request):
    if not request.user.groups.filter(name='manager').exists():
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project added successfully.')
            return redirect('mdashboard')
    all_projects = Project.objects.filter(manager=request.user)
    all_project_alloted = ProjectAlotted.objects.filter(manager=request.user)
    # users that belong to group employee
    all_employees = User.objects.filter(groups__name='employee')
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
    return render(request, 'accounts/mdashboard.html', ctx)

@login_required
def emp_dashboard(request):
    if not request.user.groups.filter(name='employee').exists():
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    
    return render(request, 'accounts/employee/dashboard.html')

# views.py
from django.core.mail import send_mail

def add_employee(request):
    if request.method == 'POST':
        employee_select = request.POST.get('employeeSelect')
        new_employee_name = request.POST.get('newEmployeeName')
        
        # Send email to selected or newly added employee
        if employee_select:
            recipient_email = get_employee_email_by_id(employee_select)  # Get recipient email from database
            send_mail(
                'Subject',
                'Message body',
                'your_email@example.com',
                [recipient_email],
                fail_silently=False,
            )
        elif new_employee_name:
            send_mail(
                'Subject',
                'Message body',
                'your_email@example.com',
                [new_employee_name],
                fail_silently=False,
            )
        # Additional logic to save the employee or handle form submission
        
    return redirect('add_employee_success')  # Redirect to a success page after form submission

# views.py

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def emp_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            user =  User.objects.create_user(username=username, password=password, email=email)
            group = Group.objects.get(name='employee')
            user.groups.add(group)
            user.save()
            messages.success(request, 'Registered')
            return redirect('emp_login')  # Redirect to the employee login page after successful registration
        else:
            messages.error(request, 'Failed')
            return render(request, 'emp_register.html', {'error_message': 'Passwords do not match.'})
    return render(request, 'accounts/employee/emp_register.html')


def emp_login(request):
    # Handle employee login logic
    return render(request, 'accounts/employee/emp_login.html')

def emp_dashboard(request):
    # Handle employee dashboard logic
    return render(request, 'accounts/employee/emp_dashboard.html')

# Accounts/views.py
from django.shortcuts import render, redirect
from .forms import ProjectForm

def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mdashboard')  # Redirect to dashboard after successful submission
    else:
        form = ProjectForm()
    return render(request, 'dashboard.html', {'form': form})




