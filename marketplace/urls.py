from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("products", views.product_list, name="product_list"),
    path("categories", views.categories, name="categories"),
    path("faq", views.faq, name="faq"),
    path("sell", views.sell, name="sell"),
    path("product/<int:product_id>", views.product_detail, name="product_detail"),
    path("product/<int:product_id>/edit", views.edit_listing, name="edit_listing"),
    path("product/<int:product_id>/delete", views.delete_listing, name="delete_listing"),
    path("product/<int:product_id>/chat", views.product_chat, name="product_chat"),
    path("product/<int:product_id>/chat/report-user", views.report_chat_user, name="report_chat_user"),
    path("product/<int:product_id>/report", views.report_listing, name="report_listing"),
    path("product/<int:product_id>/review", views.submit_review, name="submit_review"),
    path("review/<int:review_id>/helpful", views.helpful_review, name="helpful_review"),
    path("cart", views.cart, name="cart"),
    path("cart/add/<int:product_id>", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:product_id>", views.update_cart, name="update_cart"),
    path("cart/remove/<int:product_id>", views.remove_from_cart, name="remove_from_cart"),
    path("checkout", views.checkout, name="checkout"),
    path("order-confirmation", views.order_confirmation, name="order_confirmation"),
    path("login", views.login, name="login"),
    path("login/verify", views.verify_login, name="verify_login"),
    path("login/resend", views.resend_login_otp, name="resend_login_otp"),
    path(
        "password-reset",
        auth_views.PasswordResetView.as_view(
            template_name="client/password_reset_form.html",
            email_template_name="client/password_reset_email.html",
            subject_template_name="client/password_reset_subject.txt",
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done",
        auth_views.PasswordResetDoneView.as_view(
            template_name="client/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset/confirm/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="client/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="client/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("register", views.register, name="register"),
    path("logout", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("register/verify", views.verify_registration, name="verify_registration"),
    path("register/resend", views.resend_registration_otp, name="resend_registration_otp"),
    path("account-settings", views.account_settings, name="account_settings"),
    path("account-settings/verify", views.verify_account_change, name="verify_account_change"),
    path("profile", views.profile, name="profile"),
    path("contact", views.contact, name="contact"),
    #path("admin/login", views.admin_login, name="admin_login"),
    #path("admin", views.admin_dashboard, name="admin_dashboard"),
    #path("admin/products/add", views.add_product, name="add_product"),
    #path("admin/products/edit/<int:product_id>", views.edit_product, name="edit_product"),
    #path("admin/orders", views.admin_orders, name="admin_orders"),
    #path("admin/order/<int:order_id>", views.admin_order_detail, name="admin_order_detail"),
    #path("admin/users", views.admin_users, name="admin_users"),
]
