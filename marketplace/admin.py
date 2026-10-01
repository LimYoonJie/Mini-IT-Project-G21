from django.contrib import admin

from .forms import ProductAdminForm
from .models import ListingReport, Product, ProductReview, Purchase, ReviewAttachment, ReviewHelpfulVote
from .models import MarketplaceOrder, MarketplaceOrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ("id", "name", "category", "price", "stock")
    search_fields = ("name", "category")


@admin.register(ListingReport)
class ListingReportAdmin(admin.ModelAdmin):
    list_display = ("product", "reason", "reporter", "status", "created_at", "reviewed_at")
    list_filter = ("status", "reason", "created_at")
    search_fields = ("product__name", "details", "reporter__email")
    list_editable = ("status",)
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

admin.site.register(Purchase)
admin.site.register(ProductReview)
admin.site.register(ReviewAttachment)
admin.site.register(ReviewHelpfulVote)
