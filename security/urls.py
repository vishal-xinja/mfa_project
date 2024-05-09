from django.urls import path
from .views import *

urlpatterns = [
    path('project/add/', add_project, name='add_project'),
    path('project/<int:pk>/', project_details, name='project_detail'),
    path('project/<int:pk>/employee/asign/', asign_employee_to_project, name='asign_employee_to_project'),
    path('project/<int:pa>/employee/remove/', remove_employee_from_project, name='remove_employee_from_project'),
    path('project/delete/<int:pk>/', delete_project, name='delete_project'),
    path('project/all', all_projects, name='all_projects'),
    path('project/<int:pk>/edit/', edit_project, name='edit_project'),
    path('project/<int:pk>/auth/set/', set_project_auth, name='set_project_auth'),
    path('project/<int:pk>/auth/edit/', edit_project_auth, name='edit_project_auth'),
    path('employee/auth/project/<int:pk>/', employee_project_auth, name='employee_project_auth'),
]