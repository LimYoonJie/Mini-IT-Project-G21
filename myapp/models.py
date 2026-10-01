from django.db import models
from django.contrib.auth.models import User
from marketplace.models import Product

# Order Table
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='myapp_buyer_orders', verbose_name="Buyer")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='myapp_product_orders', verbose_name="Product")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Final Price(RM)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Order Time")

    class Meta:
        verbose_name_plural = "Order Management"

    def __str__(self):
        return f"Order #{self.id} - {self.product.title if self.product else 'Unknown'}"