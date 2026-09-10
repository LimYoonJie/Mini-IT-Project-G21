from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("products", views.product_list, name="product_list"),
    path("product/<int:product_id>", views.product_detail, name="product_detail"),
    path("cart", views.cart, name="cart"),
    path("checkout", views.checkout, name="checkout"),
    path("order-confirmation", views.order_confirmation, name="order_confirmation"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("admin/login", views.admin_login, name="admin_login"),
    path("admin", views.admin_dashboard, name="admin_dashboard"),
    path("admin/products", views.admin_products, name="admin_products"),
    path("admin/products/add", views.add_product, name="add_product"),
    path("admin/products/edit/<int:product_id>", views.edit_product, name="edit_product"),
    path("admin/orders", views.admin_orders, name="admin_orders"),
    path("admin/order/<int:order_id>", views.admin_order_detail, name="admin_order_detail"),
    path("admin/users", views.admin_users, name="admin_users"),
]
