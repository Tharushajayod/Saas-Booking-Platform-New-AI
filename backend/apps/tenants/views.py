"""
Tenants app views.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Tenant, Owner
from .serializers import TenantSerializer, OwnerSerializer


class TenantViewSet(viewsets.ModelViewSet):
    """Tenant CRUD operations."""
    
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = (IsAuthenticated,)
    
    def perform_create(self, serializer):
        # Create tenant and associate requesting user as Owner
        tenant = serializer.save()
        try:
            Owner.objects.create(tenant=tenant, user=self.request.user)
        except Exception:
            # If owner exists or creation fails, ignore to keep API simple
            pass
    
    @action(detail=False, methods=['get'], url_path='me')
    def get_current_tenant(self, request):
        """Get current user's tenant."""
        try:
            owner = Owner.objects.get(user=request.user)
            serializer = TenantSerializer(owner.tenant)
            return Response(serializer.data)
        except Owner.DoesNotExist:
            return Response(
                {'detail': 'User has no tenant'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['patch'], url_path='me')
    def update_current_tenant(self, request):
        """Update current tenant."""
        try:
            owner = Owner.objects.get(user=request.user)
            tenant = owner.tenant
            serializer = TenantSerializer(
                tenant,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Owner.DoesNotExist:
            return Response(
                {'detail': 'User has no tenant'},
                status=status.HTTP_404_NOT_FOUND
            )
