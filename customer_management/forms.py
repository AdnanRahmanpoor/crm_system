from django import forms
from .models import Customer, Project, Document

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'company']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['customer', 'title', 'description', 'start_date', 'end_date', 'status']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file', 'customer', 'project']