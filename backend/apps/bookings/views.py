"""
Bookings API views (public booking creation + owner booking list).
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import BookingSerializer, BookingCreateSerializer
from .models import Booking, Guest
from apps.properties.models import Room
from apps.tenants.models import Owner
import uuid
from datetime import datetime


class BookingCreateView(generics.CreateAPIView):
    """Public endpoint to create a booking for a room."""

    permission_classes = (permissions.AllowAny,)
    serializer_class = BookingCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        try:
            room = Room.objects.get(id=data['room_id'])
        except Room.DoesNotExist:
            return Response({'detail': 'Room not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Compute nights
        nights = (data['check_out'] - data['check_in']).days

        # Create guest
        tenant = room.tenant
        guest = Guest.objects.create(
            tenant=tenant,
            full_name=data['guest_full_name'],
            email=data['guest_email'],
            phone=data['guest_phone']
        )

        # Create booking
        booking = Booking.objects.create(
            tenant=tenant,
            room=room,
            guest=guest,
            check_in=data['check_in'],
            check_out=data['check_out'],
            nights=nights,
            guests_count=data['guests_count'],
            room_price_per_night_lkr=room.base_price_lkr,
            total_price_lkr=room.base_price_lkr * nights,
            status='pending',
            payment_status='unpaid',
            booking_ref=f'BKG-{uuid.uuid4().hex[:8].upper()}',
            special_requests=data.get('special_requests', '')
        )

        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


class OwnerBookingListView(generics.ListAPIView):
    """List bookings for the tenant owned by the authenticated user."""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BookingSerializer

    def get_queryset(self):
        try:
            owner = Owner.objects.get(user=self.request.user)
            return Booking.objects.filter(tenant=owner.tenant).order_by('-created_at')
        except Owner.DoesNotExist:
            return Booking.objects.none()
