from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny

from reviews.models import Review
from .serializers import (CommentSerializer, ReviewSerializer)
from .permisions import IsAuthorOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        """Возвращает отзывы, относящиеся к конкретному произведению."""
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title_id=title_id)

    def get_permissions(self):
        """Определяем права доступа в зависимости от действия."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [
                permissions.IsAuthenticated, IsAuthorOrReadOnly]
        return [permission() for permission in permission_classes]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Возвращает комментарии, относящиеся к конкретному отзыву."""
        review_id = self.kwargs.get('review_id')
        return Comment.objects.filter(review_id=review_id)

    def perform_create(self, serializer):
        """Присваиваем авторство и связанный отзыв при создании комментария."""
        review_id = self.kwargs.get('review_id')
        serializer.save(author=self.request.user, review_id=review_id)

    def get_permissions(self):
        """Определяем права доступа в зависимости от действия."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [
                permissions.IsAuthenticated, IsAuthorOrReadOnly]
        return [permission() for permission in permission_classes]
