from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet): #ReadOnlyModelViewSet이 GET list, GET detail 자동으로 제공함
    queryset = Product.objects.all()
    serializer_class = ProductSerializer