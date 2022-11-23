
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

from surprise import dump
import pandas as pd
from .recommendation import get_unseen_product, recommend_product_by_userid
import os
import random
from wowstore.settings import DEBUG

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
    filterset_fields = ['=name']

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

class RecommendationView(APIView):
    def get(self, request, format=None):
        if request.user and request.user.is_authenticated:
            userId = request.user.pk % 671
        else :
            userId = random.randrange(1,671)

        file1 = "rating_matrix.pickle"
        file2 = "ratings_pred_matrix.pickle"
        if DEBUG == True:
            rating_matrix = dump.load(os.path.join('/Users/kali/BackEnd/product/', file1))
            ratings_pred_matrix = dump.load(os.path.join('/Users/kali/BackEnd/product/', file2))
        else:
            rating_matrix = dump.load(os.path.join('/home/ubuntu/resources/', file1))
            ratings_pred_matrix = dump.load(os.path.join('/home/ubuntu/resources/', file2))

        rating_matrix = list(rating_matrix)
        ratings_pred_matrix = list(ratings_pred_matrix)

        top_n = 20
        unseen_list = get_unseen_product(rating_matrix[0], userId)
        recomm_products = recommend_product_by_userid(ratings_pred_matrix[0], userId, unseen_list, top_n=top_n)
        recomm_products = pd.DataFrame(data= recomm_products.values, index=recomm_products.index, columns=['pred_score'])
        
        response = []
        for i in range(0, recomm_products.shape[0]):
            product = Product.objects.get(name=recomm_products.index[i])
            serializer = ProductSerializer(product)
            response.append(serializer.data)
        return Response(response, status=status.HTTP_200_OK)