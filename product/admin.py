from django.contrib import admin

# Register your models here.
from .models import Product, Stock, Company, Store, Event

admin.site.register(Product)
admin.site.register(Stock)
admin.site.register(Company)
admin.site.register(Store)
admin.site.register(Event)