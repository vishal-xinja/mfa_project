from django import forms

from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['picture', 'first_name', 'last_name', 'gender',  'bio']

   # dashboard/forms.py
from django import forms
from .models import Project, Employee
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Add Project'))

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'email', 'contact_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Add Employee'))

# Accounts/forms.py
from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date']