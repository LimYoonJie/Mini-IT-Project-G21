from django.conf import settings
from django.db import models


class Product(models.Model):
    CONDITION_CHOICES = [
        ("Brand New", "Brand New"),
        ("Like New", "Like New"),
        ("Lightly Used", "Lightly Used"),
        ("Well Used", "Well Used"),
        ("Heavily Used", "Heavily Used"),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, default="(category)")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.URLField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default="Lightly Used")
    created_at = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="listings",
    )

    def __str__(self):
        return self.name


class MarketplaceProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_buyer = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=True)

    def __str__(self):
        return self.user.email


class PendingRegistration(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    otp_hash = models.CharField(max_length=128)
    otp_created_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class ChatMessage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="chat_messages")
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="buyer_messages")
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="seller_messages",
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
