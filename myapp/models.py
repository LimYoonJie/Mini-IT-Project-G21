from django.db import models
from django.contrib.auth.models import User

# Product Table
class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name="Product Name")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price(RM)")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Product Image")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    sold_out = models.BooleanField(default=False, verbose_name="Is Sold Out")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Posted Date")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_products', null=True, blank=True, verbose_name="Seller")

    class Meta:
        verbose_name_plural = "Product Management"

    def __str__(self):
        return self.title


# Order Table
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='myapp_buyer_orders', verbose_name="Buyer")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='myapp_product_orders', verbose_name="Product")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Final Price(RM)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Order Time")

    class Meta:
        verbose_name_plural = "Order Management"

    def __str__(self):
        return f"Order #{self.id} - {self.product.title if self.product else 'Unknown'}"