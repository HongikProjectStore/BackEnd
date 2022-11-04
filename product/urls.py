from django.urls import path
from rest_framework import routers
from .views import CompanyViewSet, EventViewSet, LikeProductView, NearestNeighborStoreView, ProductViewSet, StoreViewSet, StockViewSet, ProductExactNameView

router = routers.SimpleRouter()
router.register('company', CompanyViewSet, basename= "company")
router.register('store', StoreViewSet, basename= "store")
router.register('stock', StockViewSet, basename= "stock")
router.register('event', EventViewSet, basename= "event")
router.register('', ProductViewSet, basename= "product")

urlpatterns = [
    path('store/distance/', NearestNeighborStoreView.as_view()),
    path('like_product/<int:pk>/', LikeProductView.as_view()),
    path('_name',ProductExactNameView.as_view()),
]

urlpatterns = urlpatterns + router.urls