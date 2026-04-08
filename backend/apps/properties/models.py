"""
Property models for rooms and availability.
"""

import uuid
from django.db import models
from apps.tenants.models import Tenant, Owner


class Property(models.Model):
    """Guest house or villa listing."""
    
    PROPERTY_TYPES = [
        ('guesthouse', 'Guest House'),
        ('villa', 'Villa'),
        ('boutique_hotel', 'Boutique Hotel'),
        ('apartment', 'Apartment'),
        ('resort', 'Resort'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='properties'
    )
    owner = models.ForeignKey(
        Owner,
        on_delete=models.SET_NULL,
        null=True,
        related_name='properties'
    )
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='Sri Lanka')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    # Media
    cover_image_url = models.URLField(blank=True, null=True)
    gallery_images = models.JSONField(default=list, help_text="Array of image URLs")
    amenities = models.JSONField(default=list, help_text="Array of amenity strings")
    
    # Publishing
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    # Rating
    rating = models.FloatField(default=0, help_text="Average rating 0-5")
    review_count = models.IntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tenant', 'is_published']),
            models.Index(fields=['city']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.city})"


class Room(models.Model):
    """Individual room/unit in a property."""
    
    ROOM_TYPES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('deluxe', 'Deluxe'),
        ('family', 'Family'),
        ('suite', 'Suite'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='rooms'
    )
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='rooms'
    )
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    room_type = models.CharField(max_length=50, choices=ROOM_TYPES, blank=True)
    
    # Capacity
    capacity = models.PositiveIntegerField(help_text="Maximum number of guests")
    beds = models.PositiveIntegerField(default=1)
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1, default=1)
    
    # Pricing
    base_price_lkr = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Base nightly rate in LKR"
    )
    
    # Media
    gallery_images = models.JSONField(default=list, help_text="Array of image URLs")
    amenities = models.JSONField(default=list, help_text="Room-specific amenities")
    
    # Availability
    is_available = models.BooleanField(default=True)
    min_nights = models.PositiveIntegerField(default=1)
    max_nights = models.PositiveIntegerField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
        unique_together = ('property', 'name')
        ordering = ['name']
        indexes = [
            models.Index(fields=['tenant', 'is_available']),
            models.Index(fields=['property']),
        ]
    
    def __str__(self):
        return f"{self.property.name} - {self.name}"


class RoomAvailability(models.Model):
    """Date-level availability/blocking for rooms."""
    
    REASON_CHOICES = [
        ('booked', 'Booked'),
        ('maintenance', 'Maintenance'),
        ('blocked', 'Manually Blocked'),
        ('unavailable', 'Unavailable'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='room_availability'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='availability'
    )
    
    date = models.DateField()
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    note = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Room Availability'
        verbose_name_plural = 'Room Availability'
        unique_together = ('room', 'date')
        ordering = ['date']
        indexes = [
            models.Index(fields=['tenant', 'date']),
            models.Index(fields=['room', 'date']),
        ]
    
    def __str__(self):
        return f"{self.room.name} - {self.date} ({self.reason})"


class SeasonalPricing(models.Model):
    """Seasonal price overrides for rooms."""
    
    SEASON_TYPES = [
        ('peak', 'Peak Season'),
        ('low', 'Low Season'),
        ('holiday', 'Holiday'),
        ('custom', 'Custom'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='seasonal_pricing'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='seasonal_prices'
    )
    
    start_date = models.DateField()
    end_date = models.DateField()
    price_lkr = models.DecimalField(max_digits=12, decimal_places=2)
    season_type = models.CharField(max_length=50, choices=SEASON_TYPES)
    label = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Seasonal Pricing'
        verbose_name_plural = 'Seasonal Pricing'
        ordering = ['start_date']
        indexes = [
            models.Index(fields=['tenant', 'start_date', 'end_date']),
            models.Index(fields=['room']),
        ]
    
    def __str__(self):
        return f"{self.room.name} - {self.start_date} to {self.end_date}"
