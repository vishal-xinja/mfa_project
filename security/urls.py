from django.urls import path
from .views import *

urlpatterns = [
    path('project/add/', add_project, name='add_project'),
    path('project/<int:pk>/', project_details, name='project_details'),
]