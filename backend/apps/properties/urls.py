"""
URL configuration for properties app.
"""

from django.urls import path
from .views import PropertyListView, PropertyDetailView, PropertyCreateView

urlpatterns = [
    path('', PropertyListView.as_view(), name='property-list'),
    path('create/', PropertyCreateView.as_view(), name='property-create'),
    path('<uuid:pk>/', PropertyDetailView.as_view(), name='property-detail'),
]
