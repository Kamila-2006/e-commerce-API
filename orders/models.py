from django.db import models
from products.models import Product


class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('processing', 'Сборка'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]

    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_address = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    @property
    def total_price(self):
        return sum(item.calculate_total for item in self.order_items.all())

    def __str__(self):
        return f"Заказ №{self.id} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)

    @property
    def calculate_total(self):
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.price = self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} штук"