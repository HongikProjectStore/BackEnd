from rest_framework import serializers

from authentication.serializers import ProfileSerializer
from .models import Board, Comment

class CommentSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ("pk","author","board","text")

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("board", "text")

class BoardSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only = True) # nested serializer
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Board
        fields = ("pk","author","title","category","body","image","published_date", "likes","views","comments")

class BoardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ("title","category","body","image")