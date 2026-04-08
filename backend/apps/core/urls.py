"""
URL configuration for core app (Authentication).
"""

from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    UserProfileView,
    ChangePasswordView,
    PasswordResetRequestView,
    HealthCheckView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('health/', HealthCheckView.as_view(), name='health-check'),
]
