from datetime import datetime, timedelta

from django.db import models
from django.conf import settings


# from TechFort.products.models import Product

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    item = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_purchased = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quantity} X {self.item}'

    def get_total(self):
        total_amount = self.item.new_price * self.quantity
        float_total = format(total_amount, '0.2f')
        return float_total


class Coupon(models.Model):
    code = models.CharField(max_length=10, unique=True, blank=True)
    valid_from = models.DateTimeField(default=datetime.now, blank=True)
    valid_to = models.DateTimeField(default=(datetime.now() + timedelta(days=7)))
    discount = models.IntegerField(default=15)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class Order(models.Model):
    order_items = models.ManyToManyField(Cart)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_order = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_date = models.CharField(default="within 3 days", max_length=200, blank=True, null=True)
    payment_id = models.CharField(max_length=264, blank=True, null=True)
    order_id = models.CharField(max_length=200, blank=True, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, blank=True, null=True)
    vat = models.FloatField(default=0.0, verbose_name="VAT")

    def get_sub_total_price(self):
        total = 0
        for item in self.order_items.all():
            total += float(item.get_total())
        return total

    def get_total_price(self):
        total = self.get_sub_total_price()
        if self.coupon and self.coupon.valid_to < datetime.now():
            total = total * (1 - self.coupon.discount / 100)

        final_amount = total * (1 + self.vat / 100)
        return final_amount
