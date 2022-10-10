from authentication.models import User
from django.db import models
from django.utils import timezone

EVENT_TYPE = (
    ('1+1', '1+1'),
    ('2+1', '2+1'),
    ('3+1', '2+1'),
    ('DC','Discount'),
    ('DUM','Dummy'),
)

PRODUCT_KIND = (
    ('Meal','Meal'),
    ('Food','Food'),        
    ('Bakery','Bakery'),
    ('Beverage','Beverage'),
    ('DairyProduct','DairyProduct'),
    ('Snack','Snack'),
    ('Icecream','Icecream'),
    ('Necessaries','Necessaries'),
    ('Etc','Etc'),
)

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=128)
    kind = models.CharField(max_length=12, choices=PRODUCT_KIND)
    manufacturer = models.CharField(max_length=128)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', default='default_product.png')
    likes = models.ManyToManyField(User, related_name='like_products', blank=True)

    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Store(models.Model):
    company = models.ForeignKey(Company, related_name='stores', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    store = models.ForeignKey(Store,related_name='stocks', on_delete=models.CASCADE)
    counts = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'store'], name='stock_id')
        ]

    def __str__(self):
        return self.counts

class Event(models.Model):
    product = models.ForeignKey(Product, related_name='events', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=3, choices=EVENT_TYPE)
    description = models.TextField(default='')
    start_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'company'], name='event_id')
        ]

    def __str__(self):
        return self.event_type