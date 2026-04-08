"""
Core app serializers for authentication.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Minimal user information serializer."""
    
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'email_verified')
        read_only_fields = ('id', 'email_verified')


class RegisterSerializer(serializers.ModelSerializer):
    """User registration serializer."""
    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'password', 'password2')
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        email = validated_data.get('email')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', '')
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Login request serializer."""
    
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    """Change password serializer."""
    
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password2 = serializers.CharField(write_only=True)
    
    def validate(self, data):
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data


class PasswordResetRequestSerializer(serializers.Serializer):
    """Password reset request serializer."""
    
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Password reset confirmation serializer."""
    
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password2 = serializers.CharField(write_only=True)
    
    def validate(self, data):
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
