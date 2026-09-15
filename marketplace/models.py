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
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)
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
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)

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


class ListingReport(models.Model):
    REASON_CHOICES = [
        ("offensive", "Offensive behavior/content"),
        ("suspicious", "Suspicious account"),
        ("counterfeit", "Selling counterfeit items"),
        ("duplicate", "Duplicate posts"),
        ("prohibited", "Selling prohibited item"),
        ("mispriced", "Mispriced listing"),
        ("category", "Item wrongly categorized"),
        ("keywords", "Irrelevant keywords"),
        ("other", "Other"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reports")
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="listing_reports",
    )
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Report for {self.product} ({self.get_reason_display()})"
