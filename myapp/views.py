from django.shortcuts import render, get_object_or_404
from .models import Product
from .models import Order

def home(request):
    return render(request, "home.html")

def products(request):
    products = Product.objects.all()
    return render(request, "products.html", {"products": products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product-details.html", {"product": product})

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

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