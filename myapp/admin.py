from django.contrib import admin
from django.contrib.auth.models import User
from marketplace.models import Product
from .models import Order

# Admin site header
admin.site.site_header = 'MMU Second-hand Marketplace Admin'

# Admin dashboard
class MyAdminSite(admin.AdminSite):
    index_template = 'admin/index.html'
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['total_users'] = User.objects.count()
        extra_context['total_listings'] = Product.objects.count()
        return super().index(request, extra_context=extra_context)

admin.site.__class__ = MyAdminSite


# Admin product management
@admin.register(Product)
class ProductManagementAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'stock')
    list_filter = ('category',)
    search_fields = ('name', 'category')
    actions = ['force_out_of_stock']

    def force_out_of_stock(self, request, queryset):
        queryset.update(stock=0)
        self.message_user(request, "Success: Selected violating items have been forcefully taken down (Stock cleared).")
    force_out_of_stock.short_description = "Force take down selected items (Violation)"


# ban/unban users
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'is_staff')
    list_filter = ('is_active',)
    search_fields = ('username', 'email')
    actions = ['ban_users', 'unban_users']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        return qs.filter(is_superuser=False, is_staff=False)



    def ban_users(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Success: Selected user accounts have been strictly BANNED.")
    ban_users.short_description = "Ban selected user accounts"


    def unban_users(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Success: Selected user accounts have been reactivated.")
    unban_users.short_description = "Reactivate selected user accounts"

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# Admin order management
@admin.register(Order)
class OrderManagementAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'product', 'price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    actions = ['mark_as_completed', 'mark_as_cancelled']

    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
        self.message_user(request, "Selected orders have been marked as Completed.")
    mark_as_completed.short_description = "Mark selected orders as Completed"

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, "Selected orders have been marked as Cancelled.")
    mark_as_cancelled.short_description = "Mark selected orders as Cancelled"
