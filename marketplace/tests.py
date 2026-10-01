from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import MarketplaceOrder, MarketplaceOrderItem, Product, ProductReview, Purchase, ReviewHelpfulVote

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


class StripeCheckoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="buyer",
            email="buyer@student.mmu.edu.my",
            password="Password123",
        )
        self.client.login(username=self.user.username, password="Password123")
        self.product = Product.objects.create(
            name="Desk lamp",
            category="Home",
            price=Decimal("25.50"),
            stock=2,
        )
        session = self.client.session
        session["cart"] = {str(self.product.pk): 1}
        session.save()

    @override_settings(STRIPE_SECRET_KEY="sk_test_demo")
    @patch("marketplace.views.stripe.checkout.Session.create")
    def test_checkout_creates_pending_order_and_reserves_stock(self, create_session):
        create_session.return_value = SimpleNamespace(
            id="cs_test_demo",
            url="https://checkout.stripe.test/session",
        )

        response = self.client.post(reverse("checkout"))

        self.assertRedirects(response, "https://checkout.stripe.test/session", fetch_redirect_response=False)
        order = MarketplaceOrder.objects.get(buyer=self.user)
        self.assertEqual(order.status, MarketplaceOrder.Status.PENDING)
        self.assertEqual(order.total, Decimal("25.50"))
        self.assertEqual(order.stripe_session_id, "cs_test_demo")
        self.assertEqual(self.product.__class__.objects.get(pk=self.product.pk).stock, 1)
        create_session.assert_called_once()

    @override_settings(STRIPE_SECRET_KEY="")
    def test_checkout_without_stripe_key_does_not_create_order_or_reserve_stock(self):
        response = self.client.post(reverse("checkout"))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(MarketplaceOrder.objects.exists())
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 2)

    @override_settings(STRIPE_WEBHOOK_SECRET="whsec_demo")
    @patch("marketplace.views.stripe.Webhook.construct_event")
    def test_paid_webhook_marks_order_paid_idempotently(self, construct_event):
        order = MarketplaceOrder.objects.create(
            buyer=self.user,
            total=Decimal("25.50"),
            stripe_session_id="cs_test_demo",
        )
        MarketplaceOrderItem.objects.create(
            order=order,
            product=self.product,
            product_name=self.product.name,
            unit_price=self.product.price,
        )
        construct_event.return_value = {
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "id": "cs_test_demo",
                    "metadata": {"order_id": str(order.pk)},
                    "payment_status": "paid",
                }
            },
        }

        first_response = self.client.post(
            reverse("stripe_webhook"),
            data="{}",
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="test-signature",
        )
        second_response = self.client.post(
            reverse("stripe_webhook"),
            data="{}",
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="test-signature",
        )

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)
        order.refresh_from_db()
        self.assertEqual(order.status, MarketplaceOrder.Status.PAID)
        self.assertIsNotNone(order.paid_at)

    @override_settings(STRIPE_WEBHOOK_SECRET="whsec_demo")
    @patch("marketplace.views.stripe.Webhook.construct_event")
    def test_expired_webhook_cancels_order_and_releases_stock_once(self, construct_event):
        self.product.stock = 1
        self.product.save(update_fields=["stock"])
        order = MarketplaceOrder.objects.create(
            buyer=self.user,
            total=Decimal("25.50"),
            stripe_session_id="cs_test_expired",
        )
        MarketplaceOrderItem.objects.create(
            order=order,
            product=self.product,
            product_name=self.product.name,
            unit_price=self.product.price,
        )
        self.product.stock = 0
        self.product.save(update_fields=["stock"])
        construct_event.return_value = {
            "type": "checkout.session.expired",
            "data": {
                "object": {
                    "id": "cs_test_expired",
                    "metadata": {"order_id": str(order.pk)},
                }
            },
        }

        for _ in range(2):
            response = self.client.post(
                reverse("stripe_webhook"),
                data="{}",
                content_type="application/json",
                HTTP_STRIPE_SIGNATURE="test-signature",
            )
            self.assertEqual(response.status_code, 200)

        order.refresh_from_db()
        self.product.refresh_from_db()
        self.assertEqual(order.status, MarketplaceOrder.Status.CANCELLED)
        self.assertEqual(self.product.stock, 1)


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
