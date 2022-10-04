from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
from .models import Cart, Order
# from TechFort.apps.products import Product
from ..products.models import Product


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    # current item
    cart_item = Cart.objects.get_or_create(item=item, user=request.user, is_purchased=False)
    # list of orders where is_order = False /// check for already existing order
    my_orders = Order.objects.filter(user=request.user, order_id=None, payment_id=None)
    # print(f"{request}  request")
    # print(f"pk =  {pk}")
    if my_orders.exists():
        order = my_orders[0]
        if order.order_items.filter(item=item).exists():
            cart_item[0].quantity += 1
            cart_item[0].save()
            messages.info(request, "Quantity of this item is updated.")
            return redirect("products:shop")
        else:
            order.order_items.add(cart_item[0])
            messages.info(request, "{} has been added to your cart.".format(cart_item[0].item.name))
            return redirect("products:shop")
    else:
        order = Order(user=request.user)
        order.save()
        order.order_items.add(cart_item[0])
        messages.info(request, "This item has been added to your cart.")
        return redirect("products:shop")


@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user, is_purchased=False)
    orders = Order.objects.filter(user=request.user, order_id=None, payment_id=None)
    if cart_items.exists() and orders.exists():
        order = orders[0]
        return render(request, 'order/view_cart.html', context={'cart_items': cart_items, 'order': order})
    else:
        messages.warning(request, "Your cart is empty!")
        return redirect("products:home")


@login_required
def remove_cart_item(request, pk):
    item = get_object_or_404(Product, pk=pk)
    my_order = Order.objects.filter(user=request.user, order_id=None, payment_id=None)
    if my_order.exists():
        order = my_order[0]
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, is_purchased=False)[0]
            removed_item_name = order_item.item.name
            order.order_items.remove(order_item)
            order_item.delete()
            messages.warning(request, f"Item {removed_item_name} has been removed from your cart!")
            return redirect("view_cart")
        else:
            messages.info(request, f"{item.name} was not in your cart.")
            return redirect("view_cart")
    else:
        messages.info(request, "You don't have an active order")
        return redirect("products:shop")


@login_required
def increase_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    my_orders = Order.objects.filter(user=request.user, order_id=None, payment_id=None)
    if my_orders.exists():
        order = my_orders[0]
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, is_purchased=False)[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, f"{item.name} quantity has been updated")
                return redirect("view_cart")
        else:
            messages.info(request, f"{item.name} is not in your cart")
            return redirect("products:shop")
    else:
        messages.info(request, "You don't have an active order")
        return redirect("products:shop")


@login_required
def decrease_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    my_orders = Order.objects.filter(user=request.user, order_id=None, payment_id=None)
    if my_orders.exists():
        order = my_orders[0]
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, is_purchased=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, f"{item.name} quantity has been updated")
                return redirect("view_cart")
            else:
                order.order_items.remove(order_item)
                order_item.delete()
                messages.warning(request, f"{item.name} item has been removed from your cart")
                return redirect("view_cart")
        else:
            messages.info(request, f"{item.name} is not in your cart")
            return redirect("products:home")
    else:
        messages.info(request, "You don't have an active order")
        return redirect("products:home")
