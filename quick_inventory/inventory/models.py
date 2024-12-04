from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def product_income(self):
        return self.sale_price - self.purchase_price

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('sale', 'Sale'),
        ('purchase', 'Purchase'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    quantity = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.product.name}"

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('seller', 'Seller'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='seller')

    
from django.db import models
from django.utils.timezone import now

class ClosedDay(models.Model):
    date = models.DateField(default=now)
    total_income = models.DecimalField(max_digits=10, decimal_places=2)
    total_profit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Закрытие дня: {self.date} - Доход: {self.total_income} - Прибыль: {self.total_profit}"
    

from django.db import models

class DailySale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateField()
    closed_day = models.ForeignKey(ClosedDay, on_delete=models.CASCADE, null=True, blank=True)  # Добавляем связь

    def __str__(self):
        return f'{self.product.name} - {self.quantity} sold'





