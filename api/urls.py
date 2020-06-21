from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FollowList, GroupViewSet


router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet)
router.register(r'group', GroupViewSet)


urlpatterns = [
    path('follow/', FollowList.as_view()),
    path('', include(router.urls)),
]
