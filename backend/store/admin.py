# backend/store/admin.py
from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Category, Product, Inventory, Order, OrderItem
from .services import apply_order_inventory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "category", "price", "is_active")
    list_filter = ("is_active", "category")
    search_fields = ("name", "sku")


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity", "updated_at")
    search_fields = ("product__name", "product__sku")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdminForm(forms.ModelForm):
    """
    Admin-side validation: if user tries to set an order to PAID,
    ensure there is enough stock for every OrderItem.
    """

    class Meta:
        model = Order
        fields = "__all__"

    def clean(self):
        cleaned = super().clean()
        status = cleaned.get("status")

        # Only validate stock when trying to set PAID
        if status == Order.STATUS_PAID:
            order = self.instance

            # Admin requires saving Order first before adding inlines,
            # so in practice order.pk exists when items exist.
            if order.pk:
                for item in order.items.select_related("product"):
                    inv = Inventory.objects.filter(product=item.product).first()
                    available = inv.quantity if inv else 0
                    if item.quantity > available:
                        raise forms.ValidationError(
                            f"Not enough stock for {item.product.sku}"
                        )

        return cleaned


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm
    list_display = (
        "id",
        "status",
        "customer_name",
        "customer_email",
        "created_at",
        "inventory_applied",
    )
    list_filter = ("status", "inventory_applied")
    search_fields = ("customer_name", "customer_email")
    inlines = [OrderItemInline]

    def save_model(self, request, obj, form, change):
        """
        Save the order, then if status is PAID apply inventory deduction.
        Any ValidationError from service will be shown as a form error.
        """
        super().save_model(request, obj, form, change)

        if obj.status == Order.STATUS_PAID:
            try:
                apply_order_inventory(obj)
            except ValidationError as e:
                # Attach error to the form so admin shows it nicely
                form.add_error(None, "; ".join(e.messages))
