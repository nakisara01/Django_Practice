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
    
    def save(self, *args, **kwargs):
        if self.pk: #이미 DB에 존재하는 데이터인지 검증하기 위함
            old = Product.objects.get(pk = self.pk) # get(pk = self.pk) 는 pk 즉, id를 가져오겠다는 뜻

            if old.status != self.status: #id에 해당하는 DB에 기존 저장된 상태(old.status)와 지금 저장하려는 상태(self.status)가 다를 때 상태 변경 History 생성 로직 실행
                ProductStatusHistory.objects.create(
                    product = self,
                    from_status = old.status,
                    to_status = self.status,
                    changed_by = "system",
                )

        super().save(*args, **kwargs)

    #id = models.BigAutoField(primary_key = True) 형태로 Django가 알아서 처리
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

class Investment(models.Model):

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            p = self.product
            p.current_amount += self.amount

            if p.current_amount >= p.target_amount:
                p.status = ProductStatus.CLOSED
            
            p.save()

    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = "investments")
    
    amount = models.DecimalField(
        max_digits = 15, 
        decimal_places = 0
    )

    investor_name = models.CharField(max_length = 100, default = "anonymous")
    created_at = models.DateTimeField(auto_now_add = True)
