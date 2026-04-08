"""
Tenant models for multi-tenancy.
"""

import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tenant(models.Model):
    """Master tenant/account record."""
    
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('starter', 'Starter'),
        ('professional', 'Professional'),
        ('enterprise', 'Enterprise'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, help_text="Business/Property name")
    subdomain = models.CharField(
        max_length=100,
        unique=True,
        help_text="e.g., 'palmgrove' for palmgrove.yoursaas.lk"
    )
    custom_domain = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        help_text="e.g., www.palmgrovevilla.lk (optional)"
    )
    plan = models.CharField(
        max_length=20,
        choices=PLAN_CHOICES,
        default='free'
    )
    is_active = models.BooleanField(default=True)
    logo_url = models.URLField(blank=True, null=True)
    
    # Billing
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    subscription_status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('cancelled', 'Cancelled'),
            ('past_due', 'Past Due'),
        ],
        default='active'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Tenant'
        verbose_name_plural = 'Tenants'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['subdomain']),
            models.Index(fields=['custom_domain']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.name


class Owner(models.Model):
    """Property owner user accounts."""
    
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='owners'
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='owner_profile'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='owner'
    )
    bio = models.TextField(blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    
    # Permissions
    can_manage_properties = models.BooleanField(default=True)
    can_manage_bookings = models.BooleanField(default=True)
    can_manage_staff = models.BooleanField(default=False)
    can_manage_billing = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Owner'
        verbose_name_plural = 'Owners'
        unique_together = ('tenant', 'user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} ({self.tenant.name})"
