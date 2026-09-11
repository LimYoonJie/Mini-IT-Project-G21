from django.contrib import admin
from django.contrib.auth.models import User
from .models import Product

admin.site.site_header = 'MMU Second-hand Marketplace Admin'

class MyAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['total_users'] = User.objects.count()
        extra_context['total_listings'] = Product.objects.count()
        extra_context['completed_trades'] = Product.objects.filter(sold_out=True).count()

        return super().index(request, extra_context=extra_context)

admin.site.__class__ = MyAdminSite

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'sold_out', 'date')
    list_editable = ('sold_out',)
    list_filter = ('sold_out', 'date')
    search_fields = ('title', 'description')

admin.site.register(Product, ProductAdmin)
