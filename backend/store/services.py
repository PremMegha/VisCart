from django.db import transaction
from django.core.exceptions import ValidationError

from integrations.telegram import send_telegram
from .models import Inventory, Order

LOW_STOCK_THRESHOLD = 5


def _maybe_handle_low_stock(inventory: Inventory, previous_quantity: int | None = None):
    """
    Send a low-stock alert only once when crossing threshold.
    Reset alert flag when stock goes above threshold again.
    """
    if previous_quantity is None and inventory.pk:
        previous_quantity = Inventory.objects.get(pk=inventory.pk).quantity

    prev = previous_quantity if previous_quantity is not None else inventory.quantity

    # If restocked above threshold, reset flag so future drops can alert again
    if inventory.quantity > LOW_STOCK_THRESHOLD and inventory.low_stock_alerted:
        inventory.low_stock_alerted = False
        inventory.save(update_fields=["low_stock_alerted"])
        return

    # Send alert only when crossing from above threshold to <= threshold
    crossed_down = prev > LOW_STOCK_THRESHOLD and inventory.quantity <= LOW_STOCK_THRESHOLD

    if crossed_down and not inventory.low_stock_alerted:
        msg = (
            f"⚠️ <b>LOW STOCK ALERT</b>\n"
            f"Product: <b>{inventory.product.name}</b>\n"
            f"SKU: <b>{inventory.product.sku}</b>\n"
            f"Remaining: <b>{inventory.quantity}</b>\n"
            f"Threshold: <b>{LOW_STOCK_THRESHOLD}</b>"
        )
        send_telegram(msg)

        inventory.low_stock_alerted = True
        inventory.save(update_fields=["low_stock_alerted"])


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

            prev_qty = inventory.quantity
            inventory.quantity -= item.quantity
            inventory.save()

            # ✅ Low stock check after deduction
            _maybe_handle_low_stock(inventory, previous_quantity=prev_qty)

        # Mark as applied
        order.inventory_applied = True
        order.save(update_fields=["inventory_applied"])

        # Order PAID Telegram notification
        items_lines = []
        for item in order.items.select_related("product"):
            items_lines.append(f"• {item.product.sku} × {item.quantity}")

        message = (
            f"✅ <b>ORDER PAID</b>\n"
            f"Order: <b>#{order.id}</b>\n"
            f"Customer: {order.customer_name} ({order.customer_email})\n\n"
            f"<b>Items</b>\n" + "\n".join(items_lines)
        )
        send_telegram(message)
