# hoa_tracking_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Association
from .forms import AssociationForm

def home(request):
    """Home page view, serves as dashboard for authenticated users."""
    return render(request, 'hoa_tracking_app/home.html')

# Association Management Views
@login_required
def associations(request):
    """View all associations the user has access to."""
    associations_list = Association.objects.all().order_by('name')
    return render(request, 'hoa_tracking_app/associations.html', {'associations': associations_list})

@login_required
def create_association(request):
    """Create a new homeowners association."""
    if request.method == 'POST':
        form = AssociationForm(request.POST)
        if form.is_valid():
            association = form.save()
            messages.success(request, f"Association '{association.name}' created successfully!")
            return redirect('associations')
    else:
        form = AssociationForm()
    
    return render(request, 'hoa_tracking_app/create_association.html', {'form': form})

@login_required
def association_detail(request, association_id):
    """View details of a specific association."""
    association = get_object_or_404(Association, id=association_id)
    insurance_policies = association.insurance_policies.all().order_by('expiration_date')
    state_registrations = association.state_registrations.all().order_by('expiration_date')
    compliance_notes = association.compliance_notes.all().order_by('-created_at')
    
    context = {
        'association': association,
        'insurance_policies': insurance_policies,
        'state_registrations': state_registrations,
        'compliance_notes': compliance_notes,
    }
    
    return render(request, 'hoa_tracking_app/association_detail.html', context)

# Property Management Views
@login_required
def properties(request):
    """View and manage properties."""
    # This is a placeholder - we'll implement this view later
    return render(request, 'hoa_tracking_app/properties.html')

# Board Member Management Views  
@login_required
def board(request):
    """View and manage board member information."""
    # This is a placeholder - we'll implement this view later
    return render(request, 'hoa_tracking_app/board.html')

# Report Views
@login_required
def reports(request):
    """Generate and view reports."""
    # This is a placeholder - we'll implement this view later
    return render(request, 'hoa_tracking_app/reports.html')

# User Management Views
@login_required
def profile(request):
    """View and edit user profile."""
    # This is a placeholder - we'll implement this view later
    return render(request, 'hoa_tracking_app/profile.html')

@login_required
def user_settings(request):
    """User settings and preferences."""
    # This is a placeholder - we'll implement this view later
    return render(request, 'hoa_tracking_app/settings.html')

# Information Pages
def help_page(request):
    """Help and support page."""
    # This is a placeholder - we'll implement this view later
    return render(request, 'hoa_tracking_app/help.html')

def about(request):
    """About us page."""
    # This is a placeholder - we'll implement this view later
    return render(request, 'hoa_tracking_app/about.html')

def privacy(request):
    """Privacy policy page."""
    # This is a placeholder - we'll implement this view later
    return render(request, 'hoa_tracking_app/privacy.html')

def terms(request):
    """Terms of service page."""
    # This is a placeholder - we'll implement this view later
    return render(request, 'hoa_tracking_app/terms.html')

def handler404(request, exception=None):
    """Custom 404 error handler."""
    return render(request, 'hoa_tracking_app/404.html', status=404)