from custom_users.views import SignUpView, UserViewSet, token
from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

app_name = "api"

router = routers.DefaultRouter()
router.register("categories", CategoryViewSet, basename="categories")
router.register("genres", GenreViewSet, basename="genres")
router.register("titles", TitleViewSet, basename="titles")
router.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewViewSet,
    basename="title-reviews",
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="review-comments",
)
router.register("users", UserViewSet)

auth_patterns = [
    path("auth/token/", token, name="token"),
    path("auth/signup/", SignUpView.as_view()),
]

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/", include(auth_patterns)),
]
