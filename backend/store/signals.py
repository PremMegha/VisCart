from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Product, Inventory, Order
from .services import apply_order_inventory


@receiver(post_save, sender=Product)
def create_inventory_for_product(sender, instance, created, **kwargs):
    if created:
        Inventory.objects.create(product=instance, quantity=0)


@receiver(post_save, sender=Order)
def handle_order_paid(sender, instance, created, **kwargs):
    # apply inventory when order is paid (service prevents double apply)
    if instance.status == Order.STATUS_PAID:
        apply_order_inventory(instance)
