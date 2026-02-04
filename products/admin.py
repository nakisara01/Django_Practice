from django.contrib import admin
from .models import Product
from .models import ProductStatusHistory

admin.site.register(Product)
admin.site.register(ProductStatusHistory)
