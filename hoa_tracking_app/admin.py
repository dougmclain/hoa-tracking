from django.contrib import admin
from .models import Association, InsurancePolicy, StateRegistration, ComplianceNote

class InsurancePolicyInline(admin.TabularInline):
    model = InsurancePolicy
    extra = 0

class StateRegistrationInline(admin.TabularInline):
    model = StateRegistration
    extra = 0

class ComplianceNoteInline(admin.TabularInline):
    model = ComplianceNote
    extra = 0

@admin.register(Association)
class AssociationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state')
    search_fields = ('name', 'address', 'city')
    inlines = [InsurancePolicyInline, StateRegistrationInline, ComplianceNoteInline]

@admin.register(InsurancePolicy)
class InsurancePolicyAdmin(admin.ModelAdmin):
    list_display = ('association', 'policy_type', 'provider', 'expiration_date')
    list_filter = ('policy_type', 'provider')  # Removed is_active
    search_fields = ('association__name', 'policy_number', 'provider')

@admin.register(StateRegistration)
class StateRegistrationAdmin(admin.ModelAdmin):
    list_display = ('association', 'registration_type', 'issuing_authority', 'expiration_date')
    list_filter = ('registration_type', 'issuing_authority')  # Removed is_active
    search_fields = ('association__name', 'registration_number', 'issuing_authority')

@admin.register(ComplianceNote)
class ComplianceNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'association', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description', 'association__name')