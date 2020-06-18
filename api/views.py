from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Post, Comment, Follow
from .serializers import PostSerializer, CommentSerializer, FollowSerializer
from django.shortcuts import render, get_object_or_404
from .permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user, following=request.data.following)
    def create(self, request):
        queryset = Follow.objects.all()
        save_name = self.request.query_params.get('search')
        if save_name:
            queryset = request.data.get('following')
        return queryset
    def get_queryset(self):
        queryset = Follow.objects.all()
        filter_name = self.request.query_params.get('search')
        if filter_name:
            queryset = queryset.filter(Q(user__username=filter_name) | Q(following__username=filter_name))
        return queryset  