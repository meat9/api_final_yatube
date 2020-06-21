from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers, generics, filters
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Post, Comment, Follow, Group, User
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer, CommentSerializer, FollowSerializer, GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group',]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])


class FollowList(generics.ListCreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', '=following__username']

    def perform_create(self, serializer):
        try:
            following = User.objects.get(username=self.request.data.get('following'))
            user = User.objects.get(username=self.request.user)
        except User.DoesNotExist:
            raise ValidationError('Пользователь не существует')
        try:
            follow_exist = Follow.objects.get(user=self.request.user, following = following)
            raise ValidationError('Вы уже подписаны на автора')
        except Follow.DoesNotExist:
            serializer.save(user=self.request.user, following = following)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsOwnerOrReadOnly]
