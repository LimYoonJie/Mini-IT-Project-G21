from django.contrib import admin
from django.test import TestCase

from marketplace.models import Product


class AdminRegistrationTests(TestCase):
    def test_product_registered_only_once(self):
        product_admins = [
            model for model in admin.site._registry
            if model._meta.label == Product._meta.label
        ]
        self.assertEqual(len(product_admins), 1)
