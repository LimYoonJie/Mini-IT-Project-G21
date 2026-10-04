from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import Product
from .models import Order

def home(request):
    return render(request, "home.html")

def checkout_success_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
 
    new_order = Order.objects.create(
        buyer=request.user,
        product=product,
        price=product.price,       
        status='completed' 
    )

    if hasattr(product, 'status'):
        product.status = 'sold'
        product.save()

@staff_member_required
def admin_product_view(request):
    all_products = Product.objects.all()
    return render(request, "admin_products.html", {"products": all_products})


@staff_member_required
def admin_order_view(request):
    all_orders = Order.objects.all()
    return render(request, "orders.html", {"orders": all_orders})