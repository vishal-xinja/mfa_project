from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from security.forms import ProjectForm, ProjectAlottedForm
from security.models import Project, ProjectAlotted

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


@login_required
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
            return redirect('emp_login')  # Redirect to the employee login page after successful registration
        else:
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
    context = {
        'form': form,
        'projects': Project.objects.all()
    }
    return render(request, 'accounts/mdashboard.html', context)

@login_required
def emp_dashboard(request):
    if not request.user.groups.filter(name='employee').exists():
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('home')
    
    return render(request, 'accounts/employee/dashboard.html')
