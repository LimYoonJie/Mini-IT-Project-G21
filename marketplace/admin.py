from django.contrib import admin
from .models import ListingReport, Product, ProductReview, Purchase, ReviewAttachment, ReviewHelpfulVote


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


admin.site.register(Purchase)
admin.site.register(ProductReview)
admin.site.register(ReviewAttachment)
admin.site.register(ReviewHelpfulVote)
