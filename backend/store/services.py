from django.db import transaction
from django.core.exceptions import ValidationError

from .models import Inventory, Order


def apply_order_inventory(order: Order):
    # Only for paid orders
    if order.status != Order.STATUS_PAID:
        return

    # Prevent double apply
    if order.inventory_applied:
        return

    with transaction.atomic():
        # Lock order row too (avoid race)
        order = (
            Order.objects.select_for_update()
            .prefetch_related("items__product")
            .get(pk=order.pk)
        )

        if order.inventory_applied:
            return

        # Lock each inventory row and deduct
        for item in order.items.select_related("product"):
            inventory = Inventory.objects.select_for_update().get(product=item.product)

            if inventory.quantity < item.quantity:
                raise ValidationError(f"Not enough stock for {item.product.sku}")

            inventory.quantity -= item.quantity
            inventory.save()

        # Mark as applied
        order.inventory_applied = True
        order.save(update_fields=["inventory_applied"])
