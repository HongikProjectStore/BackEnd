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
        fields = ("pk","store_id", "company", "business_name","branch_name", "address", "postcode", "longitude","latitude","stocks")

class StoreCreateSerializer(serializers.ModelSerializer):
    store_id = serializers.CharField(
        required = True,
        validators =[UniqueValidator(queryset=Store.objects.all())],
    )
    company = serializers.CharField(
        required=True
    )
    postcode = serializers.IntegerField(
        required = False,
        allow_null=True
    )

    class Meta:
        model = Store
        fields = ("store_id", "company", "business_name","branch_name", "address", "postcode", "longitude","latitude")

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("pk", "name")


class CompanyCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required = True,
        validators =[UniqueValidator(queryset=Company.objects.all())],
    )
    class Meta:
        model = Company
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):  
    events = EventSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ("pk","name","category","manufacturer", "price", "description","image", "views","likes", "events")

class ProductCreateSerializer(serializers.ModelSerializer):    
    name = serializers.CharField(
        required = True,
        validators =[UniqueValidator(queryset=Product.objects.all())],
    )
    manufacturer = serializers.CharField(
        required = False,
    )
    class Meta:
        model = Product
        fields = ("name","category","manufacturer", "price", "description","image")

