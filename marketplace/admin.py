from django.contrib import admin
from .models import ListingReport, Product


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
