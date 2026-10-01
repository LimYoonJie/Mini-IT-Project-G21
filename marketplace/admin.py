from django.contrib import admin
from .models import ListingReport, MarketplaceOrder, MarketplaceOrderItem, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price", "stock")
    search_fields = ("name", "category")


@admin.register(ListingReport)
class ListingReportAdmin(admin.ModelAdmin):
    list_display = ("product", "reason", "reporter", "created_at")
    list_filter = ("reason", "created_at")
    search_fields = ("product__name", "details", "reporter__email")
    readonly_fields = ("product", "reporter", "reason", "details", "created_at")


class MarketplaceOrderItemInline(admin.TabularInline):
    model = MarketplaceOrderItem
    extra = 0
    can_delete = False
    readonly_fields = ("product", "product_name", "unit_price", "quantity")


@admin.register(MarketplaceOrder)
class MarketplaceOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "buyer", "total", "status", "created_at", "paid_at")
    list_filter = ("status", "created_at")
    search_fields = ("buyer__email", "stripe_session_id")
    readonly_fields = ("buyer", "total", "status", "stripe_session_id", "created_at", "paid_at")
    inlines = (MarketplaceOrderItemInline,)

    def has_add_permission(self, request):
        return False
