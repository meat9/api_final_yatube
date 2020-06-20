from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Post, Comment, Follow, Group, User
from .serializers import PostSerializer, CommentSerializer, FollowSerializer, GroupSerializer
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
    #permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    def perform_create(self, serializer):
        follow = get_object_or_404(User, username=self.request.data.get('following'))
        serializer.save(user=self.request.user, following=follow)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    #permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(slug=self.kwargs['slug'], title=self.kwargs['title'])

    def get_queryset(self):
        return Group.objects.all()
        
