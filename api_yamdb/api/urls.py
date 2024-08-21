from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework import routers

from .views import ReviewViewSet, CommentViewSet

router_api_v1 = routers.DefaultRouter()
router_api_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='title-reviews'
)
router_api_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='review-comments'
)

urlpatterns = [
    path('v1/', include(router_api_v1.urls)),
]
