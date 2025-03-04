# hoa_tracking_app/compliance_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Association, InsurancePolicy, StateRegistration, ComplianceNote
from .forms import InsurancePolicyForm, StateRegistrationForm, ComplianceNoteForm

@login_required
def compliance(request):
    """View and manage compliance tracking for insurance, registrations, and licensing."""
    associations = Association.objects.all()
    insurance_policies = InsurancePolicy.objects.all().order_by('expiration_date')
    state_registrations = StateRegistration.objects.all().order_by('expiration_date')
    compliance_notes = ComplianceNote.objects.all().order_by('-created_at')
    
    # Get policies/registrations expiring soon (next 60 days)
    today = timezone.now().date()
    expiring_soon_date = today + timezone.timedelta(days=60)
    
    expiring_insurance = insurance_policies.filter(
        expiration_date__gt=today,
        expiration_date__lte=expiring_soon_date
    )
    
    expiring_registrations = state_registrations.filter(
        expiration_date__gt=today,
        expiration_date__lte=expiring_soon_date
    )
    
    context = {
        'associations': associations,
        'insurance_policies': insurance_policies,
        'state_registrations': state_registrations,
        'compliance_notes': compliance_notes,
        'expiring_insurance': expiring_insurance,
        'expiring_registrations': expiring_registrations,
    }
    
    return render(request, 'hoa_tracking_app/compliance.html', context)

@login_required
def add_insurance(request):
    """Add a new insurance policy."""
    if request.method == 'POST':
        form = InsurancePolicyForm(request.POST, request.FILES)
        if form.is_valid():
            policy = form.save()
            messages.success(request, f"Insurance policy for {policy.association.name} added successfully!")
            return redirect('compliance')
    else:
        # Pre-select association if provided in GET parameter
        initial = {}
        association_id = request.GET.get('association')
        if association_id:
            initial['association'] = association_id
        form = InsurancePolicyForm(initial=initial)
    
    return render(request, 'hoa_tracking_app/insurance_form.html', {
        'form': form,
        'title': 'Add Insurance Policy',
        'submit_text': 'Add Policy'
    })

@login_required
def view_insurance(request, policy_id):
    """View insurance policy details."""
    policy = get_object_or_404(InsurancePolicy, id=policy_id)
    return render(request, 'hoa_tracking_app/insurance_detail.html', {'policy': policy})

@login_required
def edit_insurance(request, policy_id):
    """Edit an existing insurance policy."""
    policy = get_object_or_404(InsurancePolicy, id=policy_id)
    
    if request.method == 'POST':
        form = InsurancePolicyForm(request.POST, request.FILES, instance=policy)
        if form.is_valid():
            policy = form.save()
            messages.success(request, f"Insurance policy updated successfully!")
            return redirect('compliance')
    else:
        form = InsurancePolicyForm(instance=policy)
    
    return render(request, 'hoa_tracking_app/insurance_form.html', {
        'form': form,
        'title': 'Edit Insurance Policy',
        'submit_text': 'Update Policy',
        'policy': policy
    })

@login_required
def delete_insurance(request, policy_id):
    """Delete an insurance policy."""
    policy = get_object_or_404(InsurancePolicy, id=policy_id)
    
    if request.method == 'POST':
        policy.delete()
        messages.success(request, f"Insurance policy deleted successfully!")
        return redirect('compliance')
    
    return render(request, 'hoa_tracking_app/confirm_delete.html', {
        'object': policy,
        'object_name': f"Insurance Policy: {policy.get_policy_type_display()} - {policy.association.name}",
        'cancel_url': 'compliance'
    })

@login_required
def add_registration(request):
    """Add a new state registration."""
    if request.method == 'POST':
        form = StateRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            registration = form.save()
            messages.success(request, f"Registration for {registration.association.name} added successfully!")
            return redirect('compliance')
    else:
        # Pre-select association if provided in GET parameter
        initial = {}
        association_id = request.GET.get('association')
        if association_id:
            initial['association'] = association_id
        form = StateRegistrationForm(initial=initial)
    
    return render(request, 'hoa_tracking_app/registration_form.html', {
        'form': form,
        'title': 'Add State Registration',
        'submit_text': 'Add Registration'
    })

@login_required
def view_registration(request, registration_id):
    """View registration details."""
    registration = get_object_or_404(StateRegistration, id=registration_id)
    return render(request, 'hoa_tracking_app/registration_detail.html', {'registration': registration})

@login_required
def edit_registration(request, registration_id):
    """Edit an existing registration."""
    registration = get_object_or_404(StateRegistration, id=registration_id)
    
    if request.method == 'POST':
        form = StateRegistrationForm(request.POST, request.FILES, instance=registration)
        if form.is_valid():
            registration = form.save()
            messages.success(request, f"Registration updated successfully!")
            return redirect('compliance')
    else:
        form = StateRegistrationForm(instance=registration)
    
    return render(request, 'hoa_tracking_app/registration_form.html', {
        'form': form,
        'title': 'Edit State Registration',
        'submit_text': 'Update Registration',
        'registration': registration
    })

@login_required
def delete_registration(request, registration_id):
    """Delete a registration."""
    registration = get_object_or_404(StateRegistration, id=registration_id)
    
    if request.method == 'POST':
        registration.delete()
        messages.success(request, f"Registration deleted successfully!")
        return redirect('compliance')
    
    return render(request, 'hoa_tracking_app/confirm_delete.html', {
        'object': registration,
        'object_name': f"Registration: {registration.get_registration_type_display()} - {registration.association.name}",
        'cancel_url': 'compliance'
    })

@login_required
def add_compliance_note(request):
    """Add a new compliance note."""
    if request.method == 'POST':
        form = ComplianceNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.created_by = request.user
            note.save()
            messages.success(request, "Compliance note added successfully!")
            return redirect('compliance')
    else:
        # Pre-select association if provided in GET parameter
        initial = {}
        association_id = request.GET.get('association')
        if association_id:
            initial['association'] = association_id
        form = ComplianceNoteForm(initial=initial)
    
    return render(request, 'hoa_tracking_app/note_form.html', {
        'form': form,
        'title': 'Add Compliance Note',
        'submit_text': 'Add Note'
    })

@login_required
def edit_compliance_note(request, note_id):
    """Edit an existing compliance note."""
    note = get_object_or_404(ComplianceNote, id=note_id)
    
    if request.method == 'POST':
        form = ComplianceNoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save()
            messages.success(request, "Compliance note updated successfully!")
            return redirect('compliance')
    else:
        form = ComplianceNoteForm(instance=note)
    
    return render(request, 'hoa_tracking_app/note_form.html', {
        'form': form,
        'title': 'Edit Compliance Note',
        'submit_text': 'Update Note',
        'note': note
    })

@login_required
def delete_compliance_note(request, note_id):
    """Delete a compliance note."""
    note = get_object_or_404(ComplianceNote, id=note_id)
    
    if request.method == 'POST':
        note.delete()
        messages.success(request, "Compliance note deleted successfully!")
        return redirect('compliance')
    
    return render(request, 'hoa_tracking_app/confirm_delete.html', {
        'object': note,
        'object_name': f"Compliance Note: {note.title}",
        'cancel_url': 'compliance'
    })