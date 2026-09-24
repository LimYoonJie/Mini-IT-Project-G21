from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Product, ProductReview, Purchase, ReviewHelpfulVote

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


class ProductReviewTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Desk Lamp",
            category="Lighting",
            price=Decimal("25.00"),
            stock=1,
        )
        self.buyer = User.objects.create_user(username="buyer", password="Password123")
        self.other_user = User.objects.create_user(username="other", password="Password123")

    def test_unpaid_user_cannot_review(self):
        self.client.login(username="buyer", password="Password123")

        response = self.client.post(
            reverse("submit_review", args=[self.product.id]),
            {"rating": "5", "comment": "Great lamp"},
        )

        self.assertRedirects(response, reverse("product_detail", args=[self.product.id]))
        self.assertFalse(ProductReview.objects.exists())

    def test_buyer_can_review_with_attachment(self):
        Purchase.objects.create(buyer=self.buyer, product=self.product, price=self.product.price)
        self.client.login(username="buyer", password="Password123")
        attachment = SimpleUploadedFile("receipt.txt", b"proof", content_type="text/plain")

        response = self.client.post(
            reverse("submit_review", args=[self.product.id]),
            {"rating": "5", "comment": "Great lamp", "attachments": [attachment]},
        )

        self.assertRedirects(response, reverse("product_detail", args=[self.product.id]))
        review = ProductReview.objects.get()
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.attachments.count(), 1)

    def test_helpful_vote_is_unique_and_excludes_reviewer(self):
        review = ProductReview.objects.create(
            product=self.product,
            reviewer=self.buyer,
            rating=4,
            comment="Good lamp",
        )
        self.client.login(username="other", password="Password123")

        self.client.post(reverse("helpful_review", args=[review.id]))
        self.client.post(reverse("helpful_review", args=[review.id]))

        self.assertEqual(ReviewHelpfulVote.objects.filter(review=review).count(), 1)
