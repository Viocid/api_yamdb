from django.db.models import Avg
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Genre, Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre,
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleLRSerializer(serializers.ModelSerializer):
    """Serializer для List и Retrieve."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category', 'rating')

    def get_rating(self, title):
        """Подсчет среднего рейтинга для произведения."""
        avg_score = title.reviews.aggregate(Avg('score')).get('score__avg')
        return avg_score or 0

    def validate_year(self, value):
        if value > timezone.now().year:
            raise ValidationError(
                'Год указан неверно.'
            )


class TitleCPDSerializer(serializers.ModelSerializer):
    """Serializer для Create, Partial Update and Destroy."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = Title
        fields = '__all__'
