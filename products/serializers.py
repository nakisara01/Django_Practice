from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields= [
            "id",
            "title",
            "content",
            "target_amount",
            "current_amount",
            "status",
            "created_at",
        ]