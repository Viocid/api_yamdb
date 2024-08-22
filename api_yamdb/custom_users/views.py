from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, views, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import ADMIN_EMAIL

from custom_users.permissions import IsAdmin
from custom_users.serializers import (
    AuthSerializer,
    GetTokenSerializer,
    UserAdminSerializer,
    UserSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = (IsAdmin, AllowAny)
    pagination_class = PageNumberPagination
    lookup_field = "username"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    http_method_names = ["get", "post", "patch", "delete"]

    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=[IsAuthenticated],
        serializer_class=UserSerializer,
        pagination_class=None,
    )
    def me(self, request):
        if request.method == "GET":
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@action(detail=False, permission_classes=[AllowAny])
@api_view(["POST"])
def token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=serializer.data["username"])
    if serializer.data["confirmation_code"] == user.confirmation_code:
        refresh = RefreshToken.for_user(user)
        return Response(
            {"token": str(refresh.access_token)}, status=status.HTTP_200_OK
        )
    return Response(status=status.HTTP_400_BAD_REQUEST)


class SignUpView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(
                username=request.data.get("username"),
                email=request.data.get("email"),
            )
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                "Код подтверждения",
                f"Ваш код - {confirmation_code}",
                ADMIN_EMAIL,
                [request.data.get("email")],
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
