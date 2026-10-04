from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.product_list, name="product_list"),
    path("categories", views.categories, name="categories"),
    path("faq", views.faq, name="faq"),
    path("sell", views.sell, name="sell"),
    path("product/<int:product_id>", views.product_detail, name="product_detail"),
    path("product/<int:product_id>/favorite", views.toggle_favorite, name="toggle_favorite"),
    path("product/<int:product_id>/edit", views.edit_listing, name="edit_listing"),
    path("product/<int:product_id>/delete", views.delete_listing, name="delete_listing"),
    path("product/<int:product_id>/chat", views.product_chat, name="product_chat"),
    path("inbox", views.seller_inbox, name="seller_inbox"),
    path("product/<int:product_id>/chat/report-user", views.report_chat_user, name="report_chat_user"),
    path("product/<int:product_id>/report", views.report_listing, name="report_listing"),
    path("product/<int:product_id>/review", views.submit_review, name="submit_review"),
    path("review/<int:review_id>/helpful", views.helpful_review, name="helpful_review"),
    path("cart", views.cart, name="cart"),
    path("cart/add/<int:product_id>", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:product_id>", views.update_cart, name="update_cart"),
    path("cart/remove/<int:product_id>", views.remove_from_cart, name="remove_from_cart"),
    path("checkout", views.checkout, name="checkout"),
    path("orders", views.order_history, name="order_history"),
    path("seller/orders", views.seller_orders, name="seller_orders"),
    path("seller/orders/<int:item_id>/fulfillment", views.update_fulfillment, name="update_fulfillment"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("order-confirmation", views.order_confirmation, name="order_confirmation"),
    path("stripe/webhook", views.stripe_webhook, name="stripe_webhook"),
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
    path("/internal-admin-setup/", views.quick_admin_register, name="admin_register"),
    path('backend-goods-list/', views.admin_product_view, name='backend_admin_products'),
    path('backend-sales-list/', views.admin_order_view, name='backend_admin_orders'),
    path('backend-member-list/', views.admin_user_view, name='backend_admin_users'),
    path('backend-complaint-list/', views.admin_report_view, name='backend_admin_reports'),
    path('backend-member-list/ban/<int:user_id>/', views.ban_user_action, name='ban_user_action'),
    path('backend-member-list/unban/<int:user_id>/', views.unban_user_action, name='unban_user_action'),
    path('backend-complaint-list/save/<int:report_id>/', views.save_report_status_action, name='save_report_status'),
    path('admin/register/', views.quick_admin_register, name='quick_admin_register'),
]

