from rest_framework import viewsets
from authentication.models import User

from .models import Board, Comment
from .permissions import CustomReadOnly
from .serializers import CommentCreateSerializer, CommentSerializer, BoardSerializer, BoardCreateSerializer

from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView

class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    permission_classes = [CustomReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author','likes']

    def get_serializer_class(self):
        if self.action == 'list' or 'retrieve':
            return BoardSerializer
        return BoardCreateSerializer

    def retrieve(self, request, pk):
        queryset = Board.objects.all()
        board = get_object_or_404(queryset, pk=pk)
        if self.request.user.is_authenticated:
            if request.user not in board.views.all():
                board.views.add(self.request.user)
        serializer = BoardSerializer(board)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [CustomReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author']
    
    def get_serializer_class(self):
        if self.action == 'list' or 'retrieve':
            return CommentSerializer
        return CommentCreateSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
class LikeBoardsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        board = get_object_or_404(Board,pk=pk)
        if request.user in board.likes.all():
            board.likes.remove(self.request.user)
        else:
           board.likes.add(self.request.user)
        return Response({'status':'ok'}, status=status.HTTP_200_OK)

