from django.shortcuts import get_object_or_404, render

from .models import Product


def _products():
    """Use the database while keeping the original template context name."""
    return Product.objects.all().order_by("id")


# =========================
# CLIENT ROUTES
# =========================

def home(request):
    return render(request, "client/home.html", {"products": _products()})


def product_list(request):
    return render(request, "client/products.html", {"products": _products()})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "client/product_detail.html", {"product": product})


def cart(request):
    return render(request, "client/cart.html")


def checkout(request):
    return render(request, "client/checkout.html")


def order_confirmation(request):
    return render(request, "client/order_confirmation.html")


def login(request):
    return render(request, "client/login.html")


def register(request):
    return render(request, "client/register.html")


def profile(request):
    return render(request, "client/profile.html")


# =========================
# ADMIN ROUTES
# =========================

def admin_login(request):
    return render(request, "admin/login.html")


def admin_dashboard(request):
    return render(request, "admin/dashboard.html", {"products": _products()})


def admin_products(request):
    return render(request, "admin/products.html", {"products": _products()})


def add_product(request):
    return render(request, "admin/add_product.html")


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "admin/edit_product.html", {"product": product})


def admin_orders(request):
    return render(request, "admin/orders.html")


def admin_order_detail(request, order_id):
    return render(request, "admin/order_detail.html", {"order_id": order_id})


def admin_users(request):
    return render(request, "admin/users.html")
