from authentication.models import User
from django.db import models
from django.utils import timezone

# Create your models here.
class Board(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name = 'boards')
    title = models.CharField(max_length = 128)
    category = models.CharField(max_length = 128)
    body = models.TextField()
    image = models.ImageField(upload_to='boards/', default='default.png')
    views = models.ManyToManyField(User, related_name='view_boards', blank=True)
    likes = models.ManyToManyField(User, related_name='like_boards', blank=True)
    published_date = models.DateTimeField(default=timezone.now)

class Comment(models.Model):
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    board = models.ForeignKey(Board, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)