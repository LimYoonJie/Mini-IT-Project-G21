from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-products/', views.admin_product_view, name='admin_products'),
    path('admin-order/', views.admin_order_view, name='admin_orders'),
]