# apps/properties/admin.py
from django.contrib import admin
from .models import Property, Room, RoomAvailability, SeasonalPricing

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'tenant', 'property_type', 'city', 'is_published', 'created_at')
    list_filter = ('property_type', 'is_published', 'city', 'created_at')
    search_fields = ('name', 'city')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'property', 'capacity', 'base_price_lkr', 'is_available')
    list_filter = ('is_available', 'property')
    search_fields = ('name', 'property__name')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(RoomAvailability)
class RoomAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('room', 'date', 'reason')
    list_filter = ('reason', 'date')
    search_fields = ('room__name',)

@admin.register(SeasonalPricing)
class SeasonalPricingAdmin(admin.ModelAdmin):
    list_display = ('room', 'start_date', 'end_date', 'price_lkr', 'season_type')
    list_filter = ('season_type', 'start_date')
    search_fields = ('room__name',)
