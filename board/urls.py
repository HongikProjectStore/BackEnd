from django.urls import path, re_path
from rest_framework import routers

from .views import CommentViewSet, BoardViewSet ,LikeBoardsView

router = routers.SimpleRouter()
router.register('comment', CommentViewSet, basename= "comment")
router.register('', BoardViewSet, basename= "board")

urlpatterns = router.urls + [
    path('like_board/<int:pk>/', LikeBoardsView.as_view()),
] 