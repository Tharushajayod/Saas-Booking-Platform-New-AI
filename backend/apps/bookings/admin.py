# apps/bookings/admin.py
from django.contrib import admin
from .models import Guest, Booking, Payment

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'bookings_count', 'is_vip', 'created_at')
    list_filter = ('is_vip', 'created_at')
    search_fields = ('full_name', 'email')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_ref', 'room', 'guest', 'check_in', 'check_out', 'status', 'payment_status')
    list_filter = ('status', 'payment_status', 'check_in')
    search_fields = ('booking_ref', 'guest__full_name')
    readonly_fields = ('id', 'booking_ref', 'created_at', 'updated_at')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'amount_lkr', 'method', 'status', 'created_at')
    list_filter = ('method', 'status', 'created_at')
    search_fields = ('booking__booking_ref',)
    readonly_fields = ('id', 'created_at', 'updated_at')
