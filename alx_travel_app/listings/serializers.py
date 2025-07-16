from rest_framework import serializers
from .models import Listing, Booking


class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Listing model.

    This serializer converts Listing model instances to and from JSON representations
    for use in API requests and responses.
    """

    class Meta:
        model = Listing
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Booking model.

    This serializer handles the transformation of Booking model instances
    to JSON and parsing JSON back to Booking instances for API operations.
    """

    class Meta:
        model = Booking
        fields = '__all__'
