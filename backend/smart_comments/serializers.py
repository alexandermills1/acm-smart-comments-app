# backend/smart_comments/serializers.py
from rest_framework import serializers
from .models import Post, Comment
from .classifier import classify_comment


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.IntegerField(source='post.id', read_only=True)
    flagged = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'text', 'created_at', 'flagged']
        read_only_fields = ['created_at', 'flagged']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'body']


class PostWithCommentsSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'comments']

class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['flagged']          # only the flag can be changed
        extra_kwargs = {'flagged': {'required': True}}