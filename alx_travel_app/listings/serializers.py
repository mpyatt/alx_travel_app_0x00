from rest_framework import serializers
from .models import Listing, Booking, Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.
    Automatically assigns the current user on creation.
    """
    user = serializers.StringRelatedField(read_only=True)
    listing = serializers.StringRelatedField(read_only=True)
    listing_id = serializers.PrimaryKeyRelatedField(
        queryset=Listing.objects.all(), write_only=True, source='listing'
    )

    class Meta:
        model = Review
        fields = ['id', 'user', 'listing', 'listing_id',
                  'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at', 'user', 'listing']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Listing model.
    Includes read-only nested reviews, review count, and average rating.
    """
    reviews = ReviewSerializer(many=True, read_only=True)
    reviews_count = serializers.IntegerField(
        source='reviews.count', read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = '__all__'

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews.exists():
            return None
        return round(sum([review.rating for review in reviews]) / reviews.count(), 1)


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Booking model.
    Provides readable fields for related user and listing.
    Enforces that end_date is not before start_date.
    """
    user = serializers.StringRelatedField(read_only=True)
    listing = serializers.StringRelatedField(read_only=True)
    listing_id = serializers.PrimaryKeyRelatedField(
        queryset=Listing.objects.all(), write_only=True, source='listing'
    )

    class Meta:
        model = Booking
        fields = ['id', 'user', 'listing', 'listing_id',
                  'start_date', 'end_date', 'created_at']
        read_only_fields = ['id', 'created_at', 'user', 'listing']

    def validate(self, data):
        """
        Ensure the end_date is after the start_date.
        """
        start = data.get('start_date')
        end = data.get('end_date')
        if start and end and end < start:
            raise serializers.ValidationError(
                "End date must be after start date.")
        return data

    def create(self, validated_data):
        """
        Assign the currently authenticated user to the booking.
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
