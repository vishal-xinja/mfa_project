from django.urls import path
from accounts import views as accounts_views

urlpatterns = [
    path('employee/login/', accounts_views.emp_login, name='emp_login'),
    path('employee/register/', accounts_views.emp_register, name='emp_register'),
    path('employee/logout/', accounts_views.emp_logout, name='emp_logout'),
    path('manager/login/', accounts_views.man_login, name='man_login'),
    # manager dashboard
    path('manager/dashboard/', accounts_views.mdashboard, name='mdashboard'),
    # employee dashboard
    path('employee/dashboard/', accounts_views.emp_dashboard, name='emp_dashboard'),
]
