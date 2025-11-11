# backend/smart_comments/urls.py
from django.urls import path
from .views import (
    send_the_index,
	PostCreateView,
	PostListView,
    CommentCreateView,
    FlaggedCommentsView,
	CommentUnflagView
)

urlpatterns = [
	path('', send_the_index, name='index'),
	
    path('posts/create/', PostCreateView.as_view(), name='post-create'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:post_pk>/comments/', CommentCreateView.as_view(), name='comment-create'),
    path('flagged-comments/', FlaggedCommentsView.as_view(), name='flagged-comments'),
    path('comments/<int:pk>/unflag/', CommentUnflagView.as_view(), name='comment-unflag'),
]