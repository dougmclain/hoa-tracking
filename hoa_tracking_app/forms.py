# hoa_tracking_app/forms.py
from django import forms
from .models import Association, InsurancePolicy, StateRegistration, ComplianceNote 

class AssociationForm(forms.ModelForm):
    class Meta:
        model = Association
        fields = ['name', 'address', 'city', 'state', 'zip_code', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        
class InsurancePolicyForm(forms.ModelForm):
    class Meta:
        model = InsurancePolicy
        fields = [
            'association', 'policy_type', 'policy_number', 'provider', 
            'coverage_amount', 'premium_amount', 'start_date', 
            'expiration_date', 'renewal_reminder_days', 'policy_document', 'notes'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class StateRegistrationForm(forms.ModelForm):
    class Meta:
        model = StateRegistration
        fields = [
            'association', 'registration_type', 'registration_number', 
            'issuing_authority', 'issue_date', 'expiration_date', 
            'renewal_reminder_days', 'registration_document', 'notes'
        ]
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class ComplianceNoteForm(forms.ModelForm):
    class Meta:
        model = ComplianceNote
        fields = ['association', 'title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }