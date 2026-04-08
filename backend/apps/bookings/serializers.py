"""
Bookings app serializers.
"""

from rest_framework import serializers
from .models import Guest, Booking, Payment


class GuestSerializer(serializers.ModelSerializer):
    """Guest profile serializer."""
    
    class Meta:
        model = Guest
        fields = (
            'id', 'full_name', 'email', 'phone', 'nationality',
            'date_of_birth', 'passport_number', 'bookings_count',
            'total_spent_lkr', 'is_vip', 'created_at'
        )
        read_only_fields = ('id', 'bookings_count', 'total_spent_lkr')


class PaymentSerializer(serializers.ModelSerializer):
    """Payment serializer."""
    
    class Meta:
        model = Payment
        fields = (
            'id', 'amount_lkr', 'method', 'status',
            'payhere_order_id', 'created_at', 'paid_at'
        )
        read_only_fields = ('id', 'created_at', 'paid_at')


class BookingSerializer(serializers.ModelSerializer):
    """Booking details serializer."""
    
    guest = GuestSerializer(read_only=True)
    payment = PaymentSerializer(read_only=True)
    property_name = serializers.CharField(source='room.property.name', read_only=True)
    room_name = serializers.CharField(source='room.name', read_only=True)
    
    class Meta:
        model = Booking
        fields = (
            'id', 'booking_ref', 'check_in', 'check_out', 'nights',
            'room_name', 'property_name', 'guest', 'guests_count',
            'total_price_lkr', 'status', 'payment_status',
            'special_requests', 'created_at', 'payment'
        )
        read_only_fields = ('id', 'booking_ref', 'nights', 'created_at')


class BookingCreateSerializer(serializers.Serializer):
    """Booking creation serializer (public)."""
    
    room_id = serializers.UUIDField()
    check_in = serializers.DateField()
    check_out = serializers.DateField()
    guest_full_name = serializers.CharField(max_length=255)
    guest_email = serializers.EmailField()
    guest_phone = serializers.CharField(max_length=20)
    guests_count = serializers.IntegerField(min_value=1)
    special_requests = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, data):
        if data['check_out'] <= data['check_in']:
            raise serializers.ValidationError("Check-out must be after check-in.")
        return data
