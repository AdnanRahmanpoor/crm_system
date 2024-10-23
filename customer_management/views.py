from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer, Project, Document
from .forms import CustomerForm, ProjectForm, DocumentForm

# List all customers
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_management/customer_list.html', {'customers': customers})

# creating new customer
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customer_management/customer_form.html', {'form': form})

# editing a customer
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customer_management/customer_form.html', {'form': form})

# delete a customer
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'customer_management/customer_confirm_delete.html', {'customer': customer})

# PROJECTS

# list all projects
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'customer_management/project_list.html', {'projects': projects})

# creating new project
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'customer_management/project_form.html', {'form': form})

# editing a project
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'customer_management/project_form.html', {'form': form})

# delete a project
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    return render(request, 'customer_management/project_confirm_delete.html', {'project': project})

# DOCUMENTS

def document_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, 'customer_management/document_upload.html', {'form': form})

def document_list(request, customer_id=None, project_id=None):
    if customer_id:
        documents = Document.objects.filter(customer_id=customer_id)
    elif project_id:
        documents = Document.objects.filter(project_id=project_id)
    else:
        documents = Document.objects.all()

    return render(request, 'customer_management/document_list.html', {'documents': documents})

def document_delete(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    document.delete()
    return redirect('document_list')