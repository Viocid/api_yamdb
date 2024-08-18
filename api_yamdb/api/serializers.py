from rest_framework import serializers
from django.db.models import Avg
from reviews.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author', )

    def validate(self, data):
        request = self.context.get('request')
        if request and request.method == 'POST':
            author = request.user
            title = data.get('title')
            if Review.objects.filter(author=author, title=title).exists():
                raise serializers.ValidationError(
                    "Вы уже оставляли отзыв на это произведение."
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('author', )
