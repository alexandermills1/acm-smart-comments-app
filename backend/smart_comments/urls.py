# backend/smart_comments/urls.py
from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    CommentCreateView,
    FlaggedCommentsView
)

urlpatterns = [
    # List all posts
    path('posts/', PostListView.as_view(), name='post-list'),

    # Get one post + comments
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),

    # Add comment to a post
    path('posts/<int:post_pk>/comments/', CommentCreateView.as_view(), name='comment-create'),

    # Moderator: see all flagged
    path('flagged-comments/', FlaggedCommentsView.as_view(), name='flagged-comments'),
]