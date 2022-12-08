from datetime import datetime, timedelta

from django.db import models
from django.conf import settings

from apps.account.models import User
from apps.products.models import Product


# from TechFort.products.models import Product

class Cart(models.Model):
    cart_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="Cart")
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_purchased = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quantity} X {self.item}'

    def get_total(self):
        # total_amount = 0.0
        if self.item.new_price:
            total_amount = self.item.new_price * self.quantity
        else:
            total_amount = self.item.old_price * self.quantity
        float_total = format(total_amount, '0.2f')
        return float_total

    class Meta:
        db_table = 'CART'


class Coupon(models.Model):
    code = models.CharField(max_length=10, unique=True, blank=True)
    valid_from = models.DateTimeField(default=datetime.now, blank=True)
    valid_to = models.DateTimeField(default=(datetime.now() + timedelta(days=7)))
    discount = models.IntegerField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'Coupon'


class Shipping(models.Model):
    shipping_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(User, models.DO_NOTHING, db_column='customer', blank=True, null=True)
    s_status = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    shipping_price = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'SHIPPING'


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    paid_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    accountNo = models.CharField(max_length=20, blank=False, null=False)
    expiry = models.CharField(max_length=5, blank=False, null=False)
    securityNo = models.IntegerField(blank=False, null=False)
    payment_amount = models.FloatField(blank=True, null=True)
    method = models.CharField(max_length=20, blank=True, null=True)
    pay_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'PAYMENT'


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_items = models.ManyToManyField(Cart, db_table='order_item')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='created_by')
    is_order = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    shipping = models.ForeignKey(Shipping, models.DO_NOTHING, blank=True, null=True)
    delivery_date = models.CharField(default="within 3 days", max_length=200, blank=True, null=True)
    payment = models.ForeignKey(Payment, to_field='payment_id', on_delete=models.PROTECT, blank=True, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.PROTECT, blank=True, null=True, db_column='coupon')
    vat = models.FloatField(default=2.0, verbose_name="VAT")

    def get_sub_total_price(self):
        total = 0
        for item in self.order_items.all():
            total += float(item.get_total())
        print(total)
        return total

    def get_total_price(self):
        total = self.get_sub_total_price()
        if self.coupon and self.coupon.valid_to < datetime.now():
            total = total * (1 - self.coupon.discount / 100)

        final_amount = total * (1 + self.vat / 100)
        return final_amount

    def __str__(self):
        return f'Order by {self.created_by.first_name} at {self.created_at}'
    class Meta:
        db_table = 'Order'
