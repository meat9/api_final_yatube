from django.urls import path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet


router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet)
urlpatterns = router.urls
