"""
Booking and payment models.
"""

import uuid
from django.db import models
from apps.tenants.models import Tenant
from apps.properties.models import Room


class Guest(models.Model):
    """Guest/traveler profile."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='guests'
    )
    
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    nationality = models.CharField(max_length=100, blank=True)
    
    # Optional
    date_of_birth = models.DateField(null=True, blank=True)
    passport_number = models.CharField(max_length=50, blank=True)
    
    # Guest history
    bookings_count = models.PositiveIntegerField(default=0)
    total_spent_lkr = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    is_vip = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Guest'
        verbose_name_plural = 'Guests'
        unique_together = ('tenant', 'email')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} ({self.email})"


class Booking(models.Model):
    """Booking/reservation record."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name='bookings'
    )
    guest = models.ForeignKey(
        Guest,
        on_delete=models.SET_NULL,
        null=True,
        related_name='bookings'
    )
    
    # Booking details
    check_in = models.DateField()
    check_out = models.DateField()
    nights = models.PositiveIntegerField()
    guests_count = models.PositiveIntegerField(default=1)
    
    # Pricing
    room_price_per_night_lkr = models.DecimalField(max_digits=12, decimal_places=2)
    total_price_lkr = models.DecimalField(max_digits=15, decimal_places=2)
    discount_lkr = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    taxes_lkr = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='unpaid'
    )
    
    # Reference
    booking_ref = models.CharField(
        max_length=50,
        unique=True,
        help_text="e.g., BKG-00123"
    )
    
    # Guest info
    special_requests = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tenant', 'status']),
            models.Index(fields=['booking_ref']),
            models.Index(fields=['check_in', 'check_out']),
        ]
    
    def __str__(self):
        return f"Booking {self.booking_ref}"


class Payment(models.Model):
    """Payment transaction record."""
    
    METHOD_CHOICES = [
        ('payhere', 'PayHere'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
        ('check', 'Check'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    booking = models.OneToOneField(
        Booking,
        on_delete=models.PROTECT,
        related_name='payment'
    )
    
    # Payment info
    amount_lkr = models.DecimalField(max_digits=15, decimal_places=2)
    method = models.CharField(max_length=50, choices=METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # PayHere integration (if method is payhere)
    payhere_order_id = models.CharField(max_length=255, blank=True, unique=True, null=True)
    payhere_status_code = models.IntegerField(null=True, blank=True)
    payhere_message = models.TextField(blank=True)
    payhere_md5_hash = models.CharField(max_length=255, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Refund
    refunded_at = models.DateTimeField(null=True, blank=True)
    refund_reason = models.TextField(blank=True)
    refund_amount_lkr = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tenant', 'status']),
            models.Index(fields=['booking']),
        ]
    
    def __str__(self):
        return f"Payment {self.id} - {self.amount_lkr} LKR"
