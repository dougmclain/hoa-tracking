from django.urls import path
from . import views

urlpatterns = [
    # Home and Dashboard
    path('', views.home, name='home'),
    
    # Association Management
    path('associations/', views.associations, name='associations'),
    path('associations/create/', views.create_association, name='create_association'),
    
    # Property Management
    path('properties/', views.properties, name='properties'),
    
    # Owner Management
    path('owners/', views.owners, name='owners'),
    
    # Financial Management
    path('payments/', views.payments, name='payments'),
    
    # Maintenance Management
    path('maintenance/', views.maintenance, name='maintenance'),
    
    # Meetings Management
    path('meetings/', views.meetings, name='meetings'),
    
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