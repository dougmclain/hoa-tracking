# hoa_tracking_app/urls.py
from django.urls import path
from . import views
from . import compliance_views

urlpatterns = [
    # Home and Dashboard
    path('', views.home, name='home'),
    
    # Association Management
    path('associations/', views.associations, name='associations'),
    path('associations/create/', views.create_association, name='create_association'),
    path('associations/<int:association_id>/', views.association_detail, name='association_detail'),
    
    # Property Management
    path('properties/', views.properties, name='properties'),
    
    # Compliance Management
    path('compliance/', compliance_views.compliance, name='compliance'),
    path('compliance/insurance/add/', compliance_views.add_insurance, name='add_insurance'),
    path('compliance/insurance/<int:policy_id>/', compliance_views.view_insurance, name='view_insurance'),
    path('compliance/insurance/<int:policy_id>/edit/', compliance_views.edit_insurance, name='edit_insurance'),
    path('compliance/insurance/<int:policy_id>/delete/', compliance_views.delete_insurance, name='delete_insurance'),
    
    path('compliance/registration/add/', compliance_views.add_registration, name='add_registration'),
    path('compliance/registration/<int:registration_id>/', compliance_views.view_registration, name='view_registration'),
    path('compliance/registration/<int:registration_id>/edit/', compliance_views.edit_registration, name='edit_registration'),
    path('compliance/registration/<int:registration_id>/delete/', compliance_views.delete_registration, name='delete_registration'),
    
    path('compliance/note/add/', compliance_views.add_compliance_note, name='add_compliance_note'),
    path('compliance/note/<int:note_id>/edit/', compliance_views.edit_compliance_note, name='edit_compliance_note'),
    path('compliance/note/<int:note_id>/delete/', compliance_views.delete_compliance_note, name='delete_compliance_note'),
    
    # Board Members
    path('board/', views.board, name='board'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
    
    # User Management
    path('profile/', views.profile, name='profile'),
    path('settings/', views.user_settings, name='settings'),
    
    # Information Pages
    path('help/', views.help_page, name='help'),
    path('about/', views.about, name='about'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
]