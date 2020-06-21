from rest_framework import serializers
from .models import Post, Comment, Follow, Group


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title', 'description')
        model = Group


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'group')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    following = serializers.ReadOnlyField(source='following.username')
    
    class Meta:
        fields = ('user', 'following')
        model = Follow
