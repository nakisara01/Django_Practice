from django.contrib import admin
from .models import Product
from .models import ProductStatusHistory
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "status",
        "target_amount",
        "current_amount",
        "created_at",
    )

@admin.register(ProductStatusHistory)
class ProductStatusHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "from_status",
        "to_status",
        "changed_at"
    )
