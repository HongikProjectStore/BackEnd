from django.urls import path
from rest_framework import routers

from .views import CommentViewSet, BoardViewSet ,LikeBoardsView

router = routers.SimpleRouter()
router.register('', BoardViewSet)
router.register('comments', CommentViewSet)

urlpatterns = router.urls + [
    path('likeBoards/<int:pk>/', LikeBoardsView.as_view()),
] 