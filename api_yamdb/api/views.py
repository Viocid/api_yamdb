from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from api.filters import TitlesFilter
from api.permissions import IsAdminOrAnyReadOnly, IsAuthorOrReadOnly
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleCPDSerializer,
    TitleLRSerializer,
)

from reviews.models import Category, Comment, Genre, Review, Title


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


class CategoryViewSet(CreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrAnyReadOnly,)
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg("reviews__score")).order_by(
        "name"
    )
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

    def get_title_id(self):
        return self.kwargs.get("title_id")

    def get_queryset(self):
        """Возвращает отзывы, относящиеся к конкретному произведению."""
        title_id = self.get_title_id()
        return Review.objects.filter(title_id=title_id)

    def perform_create(self, serializer):
        title_id = self.get_title_id()
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

    def get_review_id(self):
        return self.kwargs.get("review_id")

    def get_title_id(self):
        return self.kwargs.get("title_id")

    def get_queryset(self):
        """Возвращает комментарии, относящиеся к конкретному отзыву."""
        return Comment.objects.filter(review_id=self.get_review_id())

    def perform_create(self, serializer):
        """Присваиваем авторство и связанный отзыв при создании комментария."""
        title = get_object_or_404(Title, pk=self.get_title_id())
        review = get_object_or_404(
            Review, pk=self.get_review_id(), title_id=title
        )
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
