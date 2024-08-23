from django.db.models import Avg
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ("name", "slug")


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("name", "slug")


class TitleLRSerializer(serializers.ModelSerializer):
    """Serializer для List и Retrieve."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
            "rating",
        )

    def get_rating(self, title):
        """Подсчет среднего рейтинга для произведения."""
        avg_score = title.reviews.aggregate(Avg("score")).get("score__avg")
        return avg_score or None


class TitleCPDSerializer(serializers.ModelSerializer):
    """Serializer для Create, Partial Update and Destroy."""

    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug", queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")
        read_only_fields = ("author",)

    def validate(self, data):
        request = self.context.get("request")
        if request and request.method == "POST":
            author = request.user
            title_id = self.context["view"].kwargs.get("title_id")
            if Review.objects.filter(
                author=author, title_id=title_id
            ).exists():
                raise serializers.ValidationError(
                    "Вы уже оставляли отзыв на это произведение."
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
        read_only_fields = ("author",)


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title с расчетом рейтинга."""

    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
            "rating",
        )

    def get_rating(self, title):
        """Подсчет среднего рейтинга для произведения."""
        avg_score = title.reviews.aggregate(Avg("score")).get("score__avg")
        return avg_score or 0
