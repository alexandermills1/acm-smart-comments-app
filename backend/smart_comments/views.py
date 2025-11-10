# backend/smart_comments/views.py
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .serializers import PostWithCommentsSerializer, CommentSerializer
from .classifier import classify_comment


class PostListView(ListAPIView):
    queryset = Post.objects.all().order_by('-id')
    serializer_class = PostWithCommentsSerializer


class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostWithCommentsSerializer
    lookup_field = 'pk'


class CommentCreateView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post_id = self.kwargs['post_pk']
        post = get_object_or_404(Post, pk=post_id)
        text = serializer.validated_data['text']
        is_flagged = classify_comment(text) == "needs_review"
        serializer.save(post=post, flagged=is_flagged)


class FlaggedCommentsView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(flagged=True).select_related('post').order_by('-id')
