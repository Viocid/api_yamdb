from custom_users.views import SignUpView, UserViewSet, token
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("users", UserViewSet)

auth_patterns = [
    path("auth/token/", token, name="token"),
    path("auth/signup/", SignUpView.as_view()),
]

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/", include(auth_patterns)),
]
