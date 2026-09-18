from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Product

User = get_user_model()


class CartAccessTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Laptop",
            category="Electronics",
            price=Decimal("499.90"),
            stock=5,
        )

    def test_add_to_cart_requires_login(self):
        response = self.client.post(reverse("add_to_cart", args=[self.product.id]))
        self.assertRedirects(response, reverse("login"))

    def test_logged_in_user_can_add_to_cart(self):
        user = User.objects.create_user(
            username="demo-user",
            email="demo@student.mmu.edu.my",
            password="Password123",
        )
        self.client.login(username=user.username, password="Password123")

        response = self.client.post(reverse("add_to_cart", args=[self.product.id]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session.get("cart", {}).get(str(self.product.id)), 1)


class ProfilePageTests(TestCase):
    def test_profile_requires_login(self):
        response = self.client.get(reverse("profile"))
        self.assertRedirects(response, reverse("login") + "?next=" + reverse("profile"))

    def test_profile_lists_user_listings(self):
        user = User.objects.create_user(
            username="seller-user",
            email="seller@student.mmu.edu.my",
            password="Password123",
        )
        Product.objects.create(
            name="Used Chair",
            category="Furniture",
            price=Decimal("45.00"),
            stock=1,
            seller=user,
        )
        self.client.login(username=user.username, password="Password123")

        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Used Chair")
