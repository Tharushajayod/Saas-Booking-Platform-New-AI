"""
URL configuration for bookings app.
"""

from django.urls import path
from .views import BookingCreateView, OwnerBookingListView

urlpatterns = [
    path('create/', BookingCreateView.as_view(), name='booking-create'),
    path('owner/', OwnerBookingListView.as_view(), name='owner-bookings'),
]
