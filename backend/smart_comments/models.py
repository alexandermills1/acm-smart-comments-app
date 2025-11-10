# backend/smart_comments/models.py
from django.db import models

class Post(models.Model):
	title = models.CharField(max_length=200)
	body = models.TextField()

	def __str__(self):
		return self.title

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	author = models.CharField(max_length=100)
	text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	flagged = models.BooleanField(default=False)

	def __str__(self):
		return f'Comment by {self.author} on {self.post.title}'
