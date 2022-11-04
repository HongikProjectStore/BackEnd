
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status, filters, generics
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from authentication import views
from product.custom_filter import NearestNeighborFilterBackend
from .models import Product, Company, Stock, Store, Event
from .serializers import (
    ProductSerializer,
    ProductCreateSerializer,
    CompanySerializer,
    CompanyCreateSerializer,
    StockSerializer,
    StockCreateSerializer,
    StoreSerializer,
    StoreCreateSerializer,
    EventSerializer,
    EventCreateSerializer,
)
from .permissions import CustomReadOnly
# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [CustomReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['category',]
    ordering_fields = ['price','views','likes',]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ProductSerializer
        return ProductCreateSerializer

    def retrieve(self, request, pk):
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, pk=pk)
        if self.request.user.is_authenticated:
            if request.user not in product.views.all():
                product.views.add(self.request.user)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    permission_classes = [CustomReadOnly]
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return CompanySerializer
        return CompanyCreateSerializer

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    permission_classes = [CustomReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product', 'store']

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return StockSerializer
        return StockCreateSerializer

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    permission_classes = [CustomReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['business_name', 'branch_name', 'address']
    

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return StoreSerializer
        return StoreCreateSerializer

    def perform_create(self, serializer):
        company = Company.objects.get(name=self.request.data['company'])
        serializer.save(company=company)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    permission_classes = [CustomReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product','company']

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return EventSerializer
        return EventCreateSerializer

class LikeProductView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, format=None):
        product = get_object_or_404(Product,pk=pk)
        if request.user in product.likes.all():
            product.likes.remove(self.request.user)
        else:
           product.likes.add(self.request.user)
        return Response({'status':'ok'}, status=status.HTTP_200_OK)

class NearestNeighborStoreView(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    filter_backends = [NearestNeighborFilterBackend]

class ProductExactNameView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']

class EventProductView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.exclude(events__exact=None)