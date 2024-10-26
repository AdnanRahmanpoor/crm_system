from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer, Project, Document
from .forms import CustomerForm, ProjectForm, DocumentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail

@login_required
def dashboard(request):

    total_customers = Customer.objects.count()
    not_started_projects = Project.objects.filter(status='not_started').count()
    ongoing_projects = Project.objects.filter(status='in_progress').count()
    completed_projects = Project.objects.filter(status='completed').count()

    context = {
        'total_customers': total_customers,
        'not_started_projects': not_started_projects,
        'ongoing_projects': ongoing_projects,
        'completed_projects': completed_projects
    }

    return render(request, 'customer_management/dashboard.html', context)

# List all customers
@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_management/customer_list.html', {'customers': customers})

# creating new customer
@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customer_management/customer_form.html', {'form': form})

# view customer
@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    projects = Project.objects.filter(customer=customer)
    documents = Document.objects.filter(customer=customer)

    context = {
        'customer': customer,
        'projects': projects,
        'documents': documents,
    }

    return render(request, 'customer_management/customer_detail.html', context)

# editing a customer
@login_required
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
@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'customer_management/customer_confirm_delete.html', {'customer': customer})

# PROJECTS

# list all projects
@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'customer_management/project_list.html', {'projects': projects})

# creating new project
@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'customer_management/project_form.html', {'form': form})

# view a project
@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    documents = Document.objects.filter(project=project)

    context = {
        'project': project,
        'documents': documents,
    }

    return render(request, 'customer_management/project_detail.html', context)

# editing a project
@login_required
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
@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    return render(request, 'customer_management/project_confirm_delete.html', {'project': project})

# DOCUMENTS

@login_required
def document_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, 'customer_management/document_upload.html', {'form': form})

@login_required
def document_list(request, customer_id=None, project_id=None):
    if customer_id:
        documents = Document.objects.filter(customer_id=customer_id)
    elif project_id:
        documents = Document.objects.filter(project_id=project_id)
    else:
        documents = Document.objects.all()

    return render(request, 'customer_management/document_list.html', {'documents': documents})

@login_required
def document_delete(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    document.delete()
    return redirect('document_list')

def generate_access_link(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)

    # set or update the token expiration 
    customer.token_expiration = timezone.now() + timezone.timedelta(days=7)
    customer.save()

    # create access link
    access_link = request.build_absolute_uri(f'/customer-access/{customer.access_token}/')

    # send the link via email
    send_mail(
        'Access Your Documents',
        f'Hello {customer.name},\n\nYou can access your documents using the following link: {access_link}\n\nBest, regards,\nCRM Team',
        settings.DEFAULT_FROM_EMAIL,
        [customer.email],
        fail_silently=False,
    )

    return redirect('customer_list')

def customer_access(request, token):
    try:
        customer = Customer.objects.get(access_token=token)
        if customer.token_expiration and customer.token_expiration < timezone.now():
            return HttpResponseForbidden("This link has expired.")
        
        documents = customer.documents.all()
        return render(request, 'customer_management/customer_documents.html', {'customer': customer, 'documents': documents})
    
    except Customer.DoesNotExist:
        return HttpResponseForbidden("Invalid access link.")
    
@csrf_exempt
def upload_document(request, token):
    # Retrieve the customer based on token and validate expiration
    customer = get_object_or_404(Customer, access_token=token)
    if request.method == "POST":
        if customer.token_expiration and customer.token_expiration < timezone.now():
            return HttpResponseForbidden("This link has expired.")
    
    # process document upload
        document_file = request.FILES.get('document')
        if document_file:
            Document.objects.create(customer=customer, file=document_file)
            return redirect('customer_access', token=token)
        
    return HttpResponseForbidden("Upload failed.")