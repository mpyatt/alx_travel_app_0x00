from rest_framework import serializers
from .models import Listing, Booking, Review
from decimal import Decimal, ROUND_HALF_UP


class ReviewSerializer(serializers.ModelSerializer):
    """
    Handles serialization and deserialization of Review objects.

    - Automatically assigns the authenticated user on creation.
    - Prevents duplicate reviews by the same user for a listing.
    - Validates that rating is between 1 and 5.
    - Provides a human-readable rating label (e.g., "Excellent").
    """
    user = serializers.StringRelatedField(read_only=True)
    listing = serializers.StringRelatedField(read_only=True)
    listing_id = serializers.PrimaryKeyRelatedField(
        queryset=Listing.objects.all(), write_only=True, source='listing'
    )
    rating_label = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id', 'user', 'listing', 'listing_id',
            'rating', 'rating_label', 'comment', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'user', 'listing']

    def get_rating_label(self, obj):
        labels = {5: "Excellent", 4: "Good",
                  3: "Average", 2: "Poor", 1: "Terrible"}
        return labels.get(obj.rating, "")

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5.")
        return value

    def validate(self, data):
        """
        Prevent users from submitting more than one review per listing.
        """
        user = self.context['request'].user
        listing = data.get('listing')
        if Review.objects.filter(user=user, listing=listing).exists():
            raise serializers.ValidationError(
                "You have already reviewed this listing.")
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ListingSerializer(serializers.ModelSerializer):
    """
    Serializes Listing objects for API interaction.

    - Includes nested reviews (read-only).
    - Computes and returns average rating and review count.
    - Aggregates all fields in the Listing model.
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
        avg = sum([review.rating for review in reviews]) / reviews.count()
        return float(Decimal(avg).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializes Booking objects for creation and display.

    - Readable representation of user and listing.
    - Requires only `listing_id` for write operations.
    - Validates that the end date comes after the start date.
    - Automatically assigns the authenticated user on creation.
    """
    user = serializers.StringRelatedField(read_only=True)
    listing = serializers.StringRelatedField(read_only=True)
    listing_id = serializers.PrimaryKeyRelatedField(
        queryset=Listing.objects.all(), write_only=True, source='listing'
    )

    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'listing', 'listing_id',
            'start_date', 'end_date', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'user', 'listing']

    def validate(self, data):
        """
        Ensure that the booking end date is after the start date.
        """
        start = data.get('start_date')
        end = data.get('end_date')
        if start and end and end < start:
            raise serializers.ValidationError(
                "End date must be after start date.")
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
