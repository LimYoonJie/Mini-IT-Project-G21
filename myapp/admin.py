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

#admin.site.register(Product, ProductAdmin)

from django.contrib import admin
from .models import Product, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'sold_out', 'date')
    list_filter = ('sold_out', 'date')
    search_fields = ('title', 'description')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'product', 'price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    actions = ['mark_as_completed', 'mark_as_cancelled']

    @admin.action(description='Mark selected orders as Completed')
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
        self.message_user(request, "Selected orders have been marked as Completed.")

    @admin.action(description='Mark selected orders as Cancelled')
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, "Selected orders have been marked as Cancelled.")
