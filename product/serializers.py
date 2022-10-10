from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Product, Company, Stock, Store, Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ("pk","product","company","event_type", "description", "start_date", "due_date")

class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ("product","company","event_type", "description", "start_date", "due_date")

class StockSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Stock
        fields = ("pk","product","store","counts")

class StockCreateSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Stock
        fields = ("product","store","counts")
        
class StoreSerializer(serializers.ModelSerializer):    
    stocks = StockSerializer(many=True, read_only=True)
    class Meta:
        model = Store
        fields = ("pk","name","company","address","stocks")

class StoreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ("name", "company","address", "stocks")

class CompanySerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True, read_only=True)
    store = StoreSerializer(many=True, read_only=True)    
    class Meta:
        model = Company
        fields = ("pk", "name", "store", "events", "store")

class CompanyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):    
    events = EventSerializer(many=True, read_only=True)
    stocks = StockSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ("pk","name","kind","manufacturer", "price", "image", "likes", "events", "stocks")

class ProductCreateSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Product
        fields = ("name","kind","manufacturer", "price", "image")

