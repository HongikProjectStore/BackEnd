from django.urls import path
from rest_framework import routers
from .views import CompanyViewSet, EventViewSet, LikeProductView, ProductViewSet, StoreViewSet, StockViewSet

router = routers.SimpleRouter()
router.register('', ProductViewSet)
router.register('company', CompanyViewSet)
router.register('store', StoreViewSet)
router.register('stock', StockViewSet)
router.register('events', EventViewSet)
urlpatterns = router.urls + [
    path('likeProducts/<int:pk>/', LikeProductView.as_view()),
]
