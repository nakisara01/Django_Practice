from django.conf import settings
from django.db import models

class ProductStatus(models.TextChoices):
    DRAFT = "DRAFT", "임시저장"
    OPEN = "OPEN", "모집중"
    CLOSED = "CLOSED", "모집완료"
    EXECUTED = "EXECUTED", "대출시작"
    SETTLED = "SETTLED", "정산완료"

class Product(models.Model):
    def __str__(self):
        return f"[{self.id}] {self.title}"


    title = models.CharField(max_length = 100)
    content = models.TextField()

    target_amount = models.DecimalField(
        max_digits = 15, 
        decimal_places = 0,
        default = 100000000
    )

    current_amount = models.DecimalField(
        max_digits = 15, 
        decimal_places= 0,
        default = 0
    )

    status = models.CharField(
        max_length = 10,
        choices = ProductStatus.choices,
        default = ProductStatus.DRAFT,
        db_index = True
    )

    created_at = models.DateTimeField(auto_now_add=True)

class ProductStatusHistory(models.Model):
    def __str__(self):
        return f"{self.product.title}: {self.from_status} -> {self.to_status}"

    product = models.ForeignKey(Product, on_delete = models.CASCADE)

    from_status = models.CharField(
        max_length = 10,
        choices = ProductStatus.choices
    )

    to_status = models.CharField(
        max_length = 10,
        choices = ProductStatus.choices
    )

    changed_by = models.CharField(max_length = 100)
    changed_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank = True)
