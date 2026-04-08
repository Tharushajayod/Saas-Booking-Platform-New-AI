"""
Core app views for authentication.
"""

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model, authenticate
import logging

logger = logging.getLogger(__name__)

from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)

User = get_user_model()


class RegisterView(APIView):
    """User registration endpoint."""
    
    permission_classes = (AllowAny,)
    
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """User login endpoint."""
    
    permission_classes = (AllowAny,)
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = LoginSerializer(data=request.data)
            if not serializer.is_valid():
                logger.error(f"LoginSerializer validation failed: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            
            # Find user by email
            try:
                user = User.objects.get(email=email)
                logger.info(f"Found user: {email}")
            except User.DoesNotExist:
                logger.warning(f"User not found: {email}")
                return Response({
                    'detail': 'Invalid email or password.'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            # Check password
            if not user.check_password(password):
                logger.warning(f"Invalid password for user: {email}")
                return Response({
                    'detail': 'Invalid email or password.'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            # Generate tokens
            try:
                refresh = RefreshToken.for_user(user)
                user_data = UserSerializer(user).data
                
                return Response({
                    'user': user_data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"Error generating tokens: {str(e)}")
                return Response({
                    'detail': 'Error generating authentication tokens.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"LoginView unexpected error: {str(e)}", exc_info=True)
            return Response({
                'detail': 'An unexpected error occurred.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileView(APIView):
    """Get or update user profile."""
    
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request, *args, **kwargs):
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """Change password endpoint."""
    
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Verify old password
            if not request.user.check_password(serializer.validated_data['old_password']):
                return Response({
                    'old_password': 'Incorrect password.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Set new password
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            
            return Response({
                'detail': 'Password changed successfully.'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    """Request password reset."""
    
    permission_classes = (AllowAny,)
    
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            try:
                user = User.objects.get(email=email)
                # TODO: Generate reset token and send email
                return Response({
                    'detail': 'Password reset link sent to email.'
                })
            except User.DoesNotExist:
                # Don't reveal if email exists
                return Response({
                    'detail': 'Password reset link sent to email.'
                })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HealthCheckView(APIView):
    """Health check endpoint."""
    
    permission_classes = (AllowAny,)
    
    def get(self, request, *args, **kwargs):
        return Response({
            'status': 'healthy',
            'message': 'API is running'
        })
