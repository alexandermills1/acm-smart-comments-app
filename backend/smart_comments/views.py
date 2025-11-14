# backend/smart_comments/views.py
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    GenericAPIView,
)
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Post, Comment
from .serializers import (
    PostSerializer,
    PostWithCommentsSerializer,
    CommentSerializer,
    CommentUpdateSerializer,
)
from .classifier import classify_comment


def send_the_index(request):
    # returns the index from React Project
    the_index = open('static/index.html')
    return HttpResponse(the_index)


class PostCreateView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostListView(ListAPIView):
    queryset = Post.objects.all().order_by('-id')
    serializer_class = PostWithCommentsSerializer


class CommentCreateView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post_id = self.kwargs['post_pk']
        post = get_object_or_404(Post, pk=post_id)
        text = serializer.validated_data['text']
        
        result = classify_comment(text)

        if result == "blocked":
            return Response(
                {"error": "Comment blocked: contains dangerous content."},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_flagged = (result == "flagged")
        serializer.save(post=post, flagged=is_flagged)


class FlaggedCommentsView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(flagged=True).select_related('post').order_by('-id')


class CommentUnflagView(UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentUpdateSerializer
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)