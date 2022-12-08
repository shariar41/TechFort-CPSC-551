from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View

from ..order.models import Order, Cart
from .forms import BillingForm
from ..payment.models import BillingAddress
from django.contrib import messages

# Payment packages
import requests
# from sslcommerz_python.payment import SSLCSession
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
import socket


@login_required
def checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    print(saved_address)
    form = BillingForm(instance=saved_address)
    if request.method == "POST":
        form = BillingForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            form = BillingForm(instance=saved_address)
            messages.success(request, f"Shipping Address Saved!")
    # order_qs = Order.objects.filter(user=request.user, is_order=False)
    # print(order_qs)
    order_qs = Order.objects.filter(created_by=request.user, payment_id=None)
    order_items = order_qs[0].order_items.all()
    # print(order_items)
    order_total = order_qs[0].get_total_price()
    print(form + order_items + order_total + saved_address)
    return render(request, 'order/check_out.html',
                  context={"form": form, "order_items": order_items, "order_total": order_total,
                           "saved_address": saved_address})


class CheckoutView(LoginRequiredMixin, View):
    login_url = 'auth/login/'
    form_class = BillingForm
    template_name = 'order/check_out.html'

    # Handle GET HTTP requests
    def get(self, request, *args, **kwargs):
        saved_address = BillingAddress.objects.get_or_create(user=request.user)
        saved_address = saved_address[0]
        if not saved_address.email:
            saved_address.email = request.user.email
        if not saved_address.address:
            saved_address.address = request.user.profile.address_1
        if not saved_address.city:
            saved_address.city = request.user.profile.city

        form = self.form_class(instance=saved_address)
        # order_qs = Order.objects.filter(user=request.user, is_order=False)
        order_qs = Order.objects.filter(created_by=request.user, is_order=False, payment_id=None)
        # print(order_qs)
        order_items = order_qs[0].order_items.all()
        # print(order_items)
        order_total = order_qs[0].get_total_price()

        return render(request, self.template_name,
                      context={"form": form, "order_items": order_items, "order_total": order_total,
                               "saved_address": saved_address})

    # Handle POST GTTP requests
    def post(self, request, *args, **kwargs):
        saved_address = BillingAddress.objects.get_or_create(user=request.user)
        saved_address = saved_address[0]
        if not saved_address.email:
            saved_address.email = request.user.email
        if not saved_address.address:
            saved_address.address = request.user.profile.address_1
        if not saved_address.city:
            saved_address.city = request.user.profile.city

        form = self.form_class(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            messages.success(request, f"Shipping Address Saved!")
            return redirect('payment:payment')


@login_required
def payment(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    if not saved_address.is_fully_filled():
        messages.info(request, f"Please complete shipping address!")
        return redirect("payment:checkout")

    # if not request.user.profile.is_fully_filled():
    #     messages.info(request, f"Please complete profile details!")
    #     return redirect("account:profile", request.user.id)
    # if not saved_address.email:
    #     saved_address.email = request.user.email
    # if not saved_address.address:
    #     saved_address.address = request.user.profile.address_1
    # if not saved_address.city:
    #     saved_address.city = request.user.profile.city
    # if not saved_address.is_fully_filled():
    #     messages.info(request, f"Please save your shipping address!")
    #     return redirect("payment:checkout")
    # if not request.user.profile.address_1 or not request.user.profile.city or not request.user.profile.country:
    #     messages.info(request, f"Please complete Profile address!")
    #     return redirect("account:profile", request.user.id)
    # saved_address.save()

    order_qs = Order.objects.filter(created_by=request.user, payment_id=None)
    cart_items = Cart.objects.filter(cart_user=request.user, is_purchased=False)
    order = order_qs[0]
    order.is_order = True
    for cart_item in cart_items:
        cart_item.is_purchased = True
        cart_item.save()
    # order.payment
    # order.order_id = order.id

    order.save()
    # print(response_data)
    # return redirect(response_data['GatewayPageURL'])
    return HttpResponseRedirect(
        reverse("payment:purchase", kwargs={'val_id': 1, 'tran_id': 1}))
    # return render(request, "order/payment_completed_page.html")


@login_required
@csrf_exempt
def complete_payment_page(request):
    # print(request.POST)
    if request.method == 'POST' or request.method == 'post':
        payment_status = 'VALID'
        if payment_status == 'VALID':
            # transaction_id = 1
            # val_id = 1
            messages.success(request,
                             f"your payment of transaction id: {1} and bank transaction id: "
                             f"{1} is successful! Pages will be redirected after 5 seconds")
            return HttpResponseRedirect(
                reverse("payment:purchase", kwargs={'val_id': 1, 'tran_id': 1}))
        elif payment_status == 'FAILED':
            messages.warning(request,
                             f"Your payment is not successful")
        else:
            pass
    return render(request, "order/payment_completed_page.html")

    # status:{'VALID','FAILED'}
    # error
    # risk_title: {'Safe','Not_Safe'}
    # <QueryDict: {'tran_id': ['676083f6-b587-48af-a762-40483aa8ee9a'], 'val_id': ['2012282259170ZcUUKAUyc1mLgs'], 'amount': ['1.00'], 'card_type': ['MTBL-Mutual Trust Internet Banking'], 'store_amount': ['0.98'], 'card_no': [''], 'bank_tran_id': ['2012282259170VqZcxUIlO3oH7x'], 'status': ['VALID'], 'tran_date': ['2020-12-28 22:59:08'], 'error': [''], 'currency': ['BDT'], 'card_issuer': ['Mutual Trust Banking Limited'], 'card_brand': ['IB'], 'card_sub_brand': ['Classic'], 'card_issuer_country': ['Bangladesh'], 'card_issuer_country_code': ['BD'], 'store_id': ['techf5fe8c66344e79'], 'verify_sign': ['f328c1606d60ebed730368a0a770e4a2'], 'verify_key': ['amount,bank_tran_id,base_fair,card_brand,card_issuer,card_issuer_country,card_issuer_country_code,card_no,card_sub_brand,card_type,currency,currency_amount,currency_rate,currency_type,error,risk_level,risk_title,status,store_amount,store_id,tran_date,tran_id,val_id,value_a,value_b,value_c,value_d'], 'verify_sign_sha2': ['2e7e0f49b91613bfda818cbaec6a69b0ac7550f42abca1ef923807875a8a0fd3'], 'currency_type': ['BDT'], 'currency_amount': ['1.00'], 'currency_rate': ['1.0000'], 'base_fair': ['0.00'], 'value_a': [''], 'value_b': [''], 'value_c': [''], 'value_d': [''], 'risk_level': ['0'], 'risk_title': ['Safe']}>
    # <QueryDict: {'tran_id': ['cbec3cdb-d5a5-49d8-932f-23abbbde8650'], 'error': ['Invalid CVV'], 'status': ['FAILED'], 'bank_tran_id': ['201228230023jNO9wkMgg7vi4rD'], 'currency': ['BDT'], 'tran_date': ['2020-12-28 23:00:20'], 'amount': ['1.00'], 'store_id': ['techf5fe8c66344e79'], 'card_type': [''], 'card_no': [''], 'card_issuer': ['Mutual Trust Banking Limited'], 'card_brand': ['IB'], 'card_sub_brand': ['Classic'], 'card_issuer_country': ['Bangladesh'], 'card_issuer_country_code': ['BD'], 'currency_type': ['BDT'], 'currency_amount': ['1.00'], 'currency_rate': ['1.0000'], 'base_fair': ['0.00'], 'value_a': [''], 'value_b': [''], 'value_c': [''], 'value_d': [''], 'verify_sign': ['e04ef5e64efcd3ad5bb62c292b7499a8'], 'verify_sign_sha2': ['5d46e16b4c536f0c2d797649f3467bd373f01d884e47ecbd75331cc4be06b94a'], 'verify_key': ['amount,bank_tran_id,base_fair,card_brand,card_issuer,card_issuer_country,card_issuer_country_code,card_no,card_sub_brand,card_type,currency,currency_amount,currency_rate,currency_type,error,status,store_id,tran_date,tran_id,value_a,value_b,value_c,value_d']}>
    # <QueryDict: {'tran_id': ['26b62498-57e8-4d8d-9ee1-dc41ac66dc54'], 'val_id': ['201228230154DLWoNSq7CUWm33d'], 'amount': ['1.00'], 'card_type': ['MTBL-Mutual Trust Internet Banking'], 'store_amount': ['0.98'], 'card_no': [''], 'bank_tran_id': ['2012282301541Fo0mhGBtcE0N8B'], 'status': ['VALID'], 'tran_date': ['2020-12-28 23:00:53'], 'error': [''], 'currency': ['BDT'], 'card_issuer': ['Mutual Trust Banking Limited'], 'card_brand': ['IB'], 'card_sub_brand': ['Classic'], 'card_issuer_country': ['Bangladesh'], 'card_issuer_country_code': ['BD'], 'store_id': ['techf5fe8c66344e79'], 'verify_sign': ['3374f34b4c5ef609a49d124ae998f3d9'], 'verify_key': ['amount,bank_tran_id,base_fair,card_brand,card_issuer,card_issuer_country,card_issuer_country_code,card_no,card_sub_brand,card_type,currency,currency_amount,currency_rate,currency_type,error,risk_level,risk_title,status,store_amount,store_id,tran_date,tran_id,val_id,value_a,value_b,value_c,value_d'], 'verify_sign_sha2': ['95ee48c6bdf5cfaab37e64cf7cbf0f9756aa78227ffd430c515ff4fc337ae9cd'], 'currency_type': ['BDT'], 'currency_amount': ['1.00'], 'currency_rate': ['1.0000'], 'base_fair': ['0.00'], 'value_a': [''], 'value_b': [''], 'value_c': [''], 'value_d': [''], 'risk_level': ['1'], 'risk_title': ['Not Safe']}>


@login_required
def purchase(request, val_id, tran_id):
    order_qs = Order.objects.filter(created_by=request.user, payment_id=None)
    order = order_qs[0]
    order.is_order = True
    # order.order_id = tran_id  # order.id
    # order.payment_id = val_id
    order.save()

    cart_items = Cart.objects.filter(cart_user=request.user, is_purchased=False)
    for cart_item in cart_items:
        cart_item.is_purchased = True
        cart_item.save()
    messages.success(request,
                     f"your payment is successful!")
    return HttpResponseRedirect(reverse("products:shop"))
