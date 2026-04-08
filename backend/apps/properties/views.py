"""
Properties app API views.
"""

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Property
from .serializers import PropertyListSerializer, PropertySerializer
from apps.tenants.models import Owner


class PropertyListView(generics.ListAPIView):
    """List published properties for public browsing."""

    permission_classes = (permissions.AllowAny,)
    serializer_class = PropertyListSerializer
    queryset = Property.objects.filter(is_published=True).order_by('-created_at')


class PropertyDetailView(generics.RetrieveAPIView):
    """Retrieve a single property by ID."""

    permission_classes = (permissions.AllowAny,)
    serializer_class = PropertySerializer
    queryset = Property.objects.filter(is_published=True)


class PropertyCreateView(generics.CreateAPIView):
    """Authenticated owners can create properties for their tenant."""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PropertySerializer

    def create(self, request, *args, **kwargs):
        try:
            owner = Owner.objects.get(user=request.user)
        except Owner.DoesNotExist:
            return Response({'detail': 'User is not an owner of any tenant.'}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        data['tenant'] = str(owner.tenant.id)
        data['owner'] = str(owner.id)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
