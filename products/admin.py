from django.contrib import admin
from .models import Product
from .models import ProductStatusHistory
from .models import Investment
@admin.register(Product) #함수 정의 시 실행
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

@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "amount",
        "investor_name",
    )
