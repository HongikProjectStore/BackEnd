from django.urls import path
from rest_framework import routers
from .views import CompanyViewSet, EventViewSet, LikeProductView, ProductViewSet, StoreViewSet, StockViewSet

router = routers.SimpleRouter()
router.register('company', CompanyViewSet, basename= "company")
router.register('store', StoreViewSet, basename= "store")
router.register('stock', StockViewSet, basename= "stock")
router.register('event', EventViewSet, basename= "event")
router.register('', ProductViewSet, basename= "product")
urlpatterns = router.urls + [
    path('likeProducts/<int:pk>/', LikeProductView.as_view()),
]
