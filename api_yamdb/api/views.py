from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from reviews.models import Category, Comment, Genre, Review, Title

from api.permissions import IsAdminOrAnyReadOnly, IsAuthorOrReadOnly
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleCPDSerializer,
    TitleLRSerializer,
)
from api.filters import TitlesFilter


class CreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    pass


class GenreViewSet(CreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
    permission_classes = (IsAdminOrAnyReadOnly,)

    def destroy(self, request, slug=None):
        genre = get_object_or_404(Genre, slug=slug)
        self.check_object_permissions(request, genre)
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(CreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrAnyReadOnly,)
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)

    def destroy(self, request, slug=None):
        category = get_object_or_404(Category, slug=slug)
        self.check_object_permissions(request, category)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleCPDSerializer
    filter_backends = (DjangoFilterBackend,)
    http_method_names = ("get", "post", "patch", "delete", "head", "options")
    filterset_class = TitlesFilter
    permission_classes = (IsAdminOrAnyReadOnly,)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleLRSerializer
        return TitleCPDSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    http_method_names = ("get", "post", "patch", "delete", "head", "options")

    def get_queryset(self):
        """Возвращает отзывы, относящиеся к конкретному произведению."""
        title_id = self.kwargs.get("title_id")
        return Review.objects.filter(title_id=title_id)

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(title=title, author=self.request.user)

    def get_permissions(self):
        """Определяем права доступа в зависимости от действия."""
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        elif self.action == "create":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
        return [permission() for permission in permission_classes]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    http_method_names = ("get", "post", "patch", "delete", "head", "options")

    def get_queryset(self):
        """Возвращает комментарии, относящиеся к конкретному отзыву."""
        review_id = self.kwargs.get("review_id")
        return Comment.objects.filter(review_id=review_id)

    def perform_create(self, serializer):
        """Присваиваем авторство и связанный отзыв при создании комментария."""
        review_id = self.kwargs.get("review_id")
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        review = get_object_or_404(Review, pk=review_id, title_id=title)
        serializer.save(review=review, author=self.request.user)

    def get_permissions(self):
        """Определяем права доступа в зависимости от действия."""
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        elif self.action == "create":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
        return [permission() for permission in permission_classes]
