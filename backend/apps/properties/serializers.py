"""
Properties app serializers.
"""

from rest_framework import serializers
from .models import Property, Room, RoomAvailability, SeasonalPricing


class PropertyListSerializer(serializers.ModelSerializer):
    """Basic property list serializer."""
    
    rooms_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Property
        fields = (
            'id', 'name', 'property_type', 'city', 'cover_image_url',
            'is_published', 'rating', 'rooms_count', 'created_at'
        )
    
    def get_rooms_count(self, obj):
        return obj.rooms.count()


class PropertySerializer(serializers.ModelSerializer):
    """Full property serializer."""
    
    class Meta:
        model = Property
        fields = (
            'id', 'name', 'description', 'property_type', 'city',
            'address', 'latitude', 'longitude', 'cover_image_url',
            'gallery_images', 'amenities', 'is_published', 'rating',
            'review_count', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class RoomSerializer(serializers.ModelSerializer):
    """Room serializer."""
    
    class Meta:
        model = Room
        fields = (
            'id', 'name', 'description', 'capacity', 'beds',
            'bathrooms', 'base_price_lkr', 'gallery_images',
            'amenities', 'is_available', 'min_nights',
            'max_nights', 'created_at'
        )
        read_only_fields = ('id', 'created_at')


class RoomAvailabilitySerializer(serializers.ModelSerializer):
    """Room availability serializer."""
    
    class Meta:
        model = RoomAvailability
        fields = ('id', 'date', 'reason', 'note')


class SeasonalPricingSerializer(serializers.ModelSerializer):
    """Seasonal pricing serializer."""
    
    class Meta:
        model = SeasonalPricing
        fields = (
            'id', 'start_date', 'end_date', 'price_lkr',
            'season_type', 'label'
        )
