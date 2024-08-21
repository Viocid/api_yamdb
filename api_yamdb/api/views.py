from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets

from .permissions import IsAdminOrAnyReadOnly
from reviews.models import (
    Category,
    Genre,
    Title
)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleLRSerializer,
    TitleCPDSerializer
)


class CreateDestroyViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    pass


class GenreViewSet(CreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrAnyReadOnly,)


class CategoryViewSet(CreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrAnyReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleCPDSerializer
    filter_backends = (DjangoFilterBackend,)
    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')
    filterset_fields = ('category', 'genre', 'name', 'year')
    permission_classes = (IsAdminOrAnyReadOnly,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleLRSerializer
        return TitleCPDSerializer
