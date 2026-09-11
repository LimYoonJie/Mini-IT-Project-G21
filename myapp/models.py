from django.db import models

# Create your models here.

class Product(models.Model):
    # Name of the product
    title = models.CharField(max_length=200, verbose_name="Product Name")
    # Price
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price(RM)")
    # Image
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Product Image")
    # Description
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    # Status
    sold_out = models.BooleanField(default=False, verbose_name="Is Sold Out")
    # Date
    date = models.DateTimeField(auto_now_add=True, verbose_name="Posted Date")

    def __str__(self):
        return self.title