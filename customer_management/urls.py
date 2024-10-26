from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard')
]

urlpatterns += [
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/new/', views.customer_create, name='customer_create'),
    path('customers/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('customers/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
]

urlpatterns += [
    path('projects/', views.project_list, name='project_list'),
    path('projects/new/', views.project_create, name='project_create'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),
]

urlpatterns += [
    path('documents/', views.document_list, name='document_list'),
    path('documents/upload/', views.document_upload, name='document_upload'),
    path('documents/<int:document_id>/delete/', views.document_delete, name='document_delete'),
]

urlpatterns += [
    path('login/', auth_views.LoginView.as_view(template_name='customer_management/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

urlpatterns += [
    path('generate-access-link/<int:customer_id>/', views.generate_access_link, name='generate_access_link'),
    path('customer_access/<uuid:token>/', views.customer_access, name='customer_access'),
    path('upload_document/<uuid:token>/', views.upload_document, name='upload_document'),

]