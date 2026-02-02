from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from viscart.admin_sites import tenant_admin_site
from .models import Category, Product, Inventory, Order, OrderItem
from .services import apply_order_inventory


@admin.register(Category, site=tenant_admin_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product, site=tenant_admin_site)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "category", "price", "is_active")
    list_filter = ("is_active", "category")
    search_fields = ("name", "sku")


@admin.register(Inventory, site=tenant_admin_site)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity", "updated_at")
    search_fields = ("product__name", "product__sku")

    def save_model(self, request, obj, form, change):
        """
        Manual inventory edits should also:
        - reset low_stock_alerted when restocked above threshold
        - trigger a low-stock alert if quantity crosses down to <= threshold
        """
        prev_qty = None
        if obj.pk:
            prev_qty = Inventory.objects.get(pk=obj.pk).quantity

        super().save_model(request, obj, form, change)

        # Reuse the same low-stock logic as the order flow
        from .services import _maybe_handle_low_stock
        _maybe_handle_low_stock(obj, previous_quantity=prev_qty)


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

        if status == Order.STATUS_PAID:
            order = self.instance
            if order.pk:
                for item in order.items.select_related("product"):
                    inv = Inventory.objects.filter(product=item.product).first()
                    available = inv.quantity if inv else 0
                    if item.quantity > available:
                        raise forms.ValidationError(
                            f"Not enough stock for {item.product.sku}"
                        )

        return cleaned


@admin.register(Order, site=tenant_admin_site)
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
                form.add_error(None, "; ".join(e.messages))
