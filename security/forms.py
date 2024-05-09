from django import forms
from .models import Project, ProjectAlotted, ProjectAuth
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date']

class ProjectAlottedForm(forms.ModelForm):
    class Meta:
        model = ProjectAlotted
        fields = ['employee']

        # projects/forms.py

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'description',
            Submit('submit', 'Save')
        )

class ProjectAuthForm(forms.ModelForm):
    class Meta:
        model = ProjectAuth
        fields = '__all__'
        exclude = ['project']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'regen_time': forms.TimeInput(attrs={'type': 'time'}),
        }
        # projects/views.py