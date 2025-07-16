from rest_framework import serializers
from .models import Listing, Booking


class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Listing model.

    This serializer converts Listing model instances to and from JSON representations
    for use in API requests and responses.

    By using 'fields = "__all__"', all fields defined in the Listing model will be included
    in the serialized output, allowing full CRUD support via DRF views.
    """

    class Meta:
        model = Listing
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Booking model.

    This serializer handles the transformation of Booking model instances
    to JSON and parsing JSON back to Booking instances for API operations.

    Using 'fields = "__all__"' ensures all model fields are exposed in the API,
    which is helpful for rapid development but may need refinement for production
    to exclude sensitive fields as needed.
    """

    class Meta:
        model = Booking
        fields = '__all__'
