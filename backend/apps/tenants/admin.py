# apps/tenants/admin.py
from django.contrib import admin
from .models import Tenant, Owner

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'subdomain', 'plan', 'is_active', 'created_at')
    list_filter = ('plan', 'is_active', 'created_at')
    search_fields = ('name', 'subdomain')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'tenant', 'role', 'created_at')
    list_filter = ('role', 'tenant', 'created_at')
    search_fields = ('user__email', 'tenant__name')
    readonly_fields = ('id', 'created_at', 'updated_at')
