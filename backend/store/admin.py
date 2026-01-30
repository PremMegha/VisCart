from django.contrib import admin
from .models import Category, Product, Inventory, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name", "slug")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "sku", "price", "is_active", "category")
    list_filter = ("is_active", "category")
    search_fields = ("name", "sku")


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "quantity", "updated_at")
    search_fields = ("product__name", "product__sku")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "customer_name", "customer_email", "created_at")
    list_filter = ("status",)
    search_fields = ("customer_name", "customer_email")
    inlines = [OrderItemInline]
