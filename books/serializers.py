from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title is required.")
        return value

    def validate_author(self, value):
        if not value.strip():
            raise serializers.ValidationError("Author is required.")
        return value

    def validate_genre(self, value):
        if not value.strip():
            raise serializers.ValidationError("Genre is required.")
        return value

    def validate_publication_year(self, value):
        if value <= 0:
            raise serializers.ValidationError("Publication year must be a valid positive integer.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive decimal value.")
        return value

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock quantity should be non-negative.")
        return value

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating should be a float between 1 and 5.")
        return value
    
    def validate_email(self, value):
        """Ensure email is unique except for the current instance being updated."""
        book_id = self.instance.id if self.instance else None  # Get current book ID if updating

        # Check if any other book has the same email
        if Book.objects.filter(email=value).exclude(id=book_id).exists():
            raise serializers.ValidationError("A book with this email already exists.")

        return value
    
    