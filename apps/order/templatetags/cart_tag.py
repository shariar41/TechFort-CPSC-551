from django import template

from ..models import Order, Cart

register = template.Library()


@register.filter
def cart_total(user):
    order = Order.objects.filter(user=user, order_id=None, payment_id=None)
    # order_qs = Order.objects.filter(user=request.user, order_id=None, payment_id=None)
    carts = Cart.objects.filter(user=user, is_purchased=False)

    if order.exists() and carts.exists():
        return order[0].order_items.count()
        return {'order': order[0], 'cart': carts[0]}
    else:
        return 0


@register.filter
def cart_items(user):
    carts = Cart.objects.filter(user=user, is_purchased=False)
    if carts.exists():
        return carts
    else:
        return 0


@register.filter
def get_sub_total_price(user):
    order = Order.objects.filter(user=user, order_id=None, payment_id=None)
    if order.exists():
        return order[0].get_sub_total_price()
    else:
        return 0


@register.filter
def get_vat(user):
    order = Order.objects.filter(user=user, order_id=None, payment_id=None)
    if order.exists():
        return order[0].vat
    else:
        return 0


@register.filter
def get_total_price(user):
    order = Order.objects.filter(user=user, order_id=None, payment_id=None)
    if order.exists():
        return order[0].get_total_price()
    else:
        return 0
