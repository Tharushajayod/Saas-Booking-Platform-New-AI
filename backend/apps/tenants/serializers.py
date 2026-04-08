"""
Tenants app serializers.
"""

from rest_framework import serializers
from .models import Tenant, Owner
from apps.core.serializers import UserSerializer


class TenantSerializer(serializers.ModelSerializer):
    """Tenant serializer."""
    
    class Meta:
        model = Tenant
        fields = (
            'id', 'name', 'subdomain', 'custom_domain', 'plan',
            'is_active', 'logo_url', 'subscription_status', 'created_at'
        )
        read_only_fields = ('id', 'created_at')


class OwnerSerializer(serializers.ModelSerializer):
    """Owner serializer."""
    
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Owner
        fields = (
            'id', 'user', 'role', 'bio', 'avatar_url',
            'can_manage_properties', 'can_manage_bookings',
            'can_manage_staff', 'can_manage_billing',
            'created_at'
        )
        read_only_fields = ('id', 'created_at')
