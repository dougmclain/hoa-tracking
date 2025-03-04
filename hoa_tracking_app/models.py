from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Association(models.Model):
    """Model representing a homeowner's association"""
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class InsurancePolicy(models.Model):
    """Model for tracking association insurance policies"""
    POLICY_TYPES = [
        ('liability', 'General Liability'),
        ('property', 'Property Insurance'),
        ('directors', 'Directors & Officers'),
        ('umbrella', 'Umbrella Policy'),
        ('workers_comp', 'Workers Compensation'),
        ('flood', 'Flood Insurance'),
        ('other', 'Other'),
    ]
    
    association = models.ForeignKey(Association, on_delete=models.CASCADE, related_name='insurance_policies')
    policy_type = models.CharField(max_length=20, choices=POLICY_TYPES)
    policy_number = models.CharField(max_length=50)
    provider = models.CharField(max_length=100)
    coverage_amount = models.DecimalField(max_digits=12, decimal_places=2)
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    expiration_date = models.DateField()
    renewal_reminder_days = models.IntegerField(default=30)
    policy_document = models.FileField(upload_to='insurance_policies/', blank=True, null=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.get_policy_type_display()} - {self.association.name}"
    
    def is_active(self):
        return self.start_date <= timezone.now().date() <= self.expiration_date
    
    def days_until_expiration(self):
        if self.expiration_date < timezone.now().date():
            return -1  # Already expired
        return (self.expiration_date - timezone.now().date()).days

class StateRegistration(models.Model):
    """Model for tracking state registrations and licenses"""
    REGISTRATION_TYPES = [
        ('incorporation', 'Articles of Incorporation'),
        ('business_license', 'Business License'),
        ('tax_exempt', 'Tax Exempt Status'),
        ('annual_report', 'Annual Report'),
        ('other', 'Other'),
    ]
    
    association = models.ForeignKey(Association, on_delete=models.CASCADE, related_name='state_registrations')
    registration_type = models.CharField(max_length=20, choices=REGISTRATION_TYPES)
    registration_number = models.CharField(max_length=50)
    issuing_authority = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)  # Some registrations might not expire
    renewal_reminder_days = models.IntegerField(default=30)
    registration_document = models.FileField(upload_to='state_registrations/', blank=True, null=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.get_registration_type_display()} - {self.association.name}"
    
    def is_active(self):
        if not self.expiration_date:
            return True  # No expiration date means it's always active
        return self.issue_date <= timezone.now().date() <= self.expiration_date
    
    def days_until_expiration(self):
        if not self.expiration_date:
            return None  # No expiration
        if self.expiration_date < timezone.now().date():
            return -1  # Already expired
        return (self.expiration_date - timezone.now().date()).days

class ComplianceNote(models.Model):
    """Model for tracking general compliance notes and activities"""
    association = models.ForeignKey(Association, on_delete=models.CASCADE, related_name='compliance_notes')
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title