from django.contrib import admin
from .models import Cart, Order, Coupon, Shipping, Payment

admin.site.register(Cart)
admin.site.register(Coupon)
admin.site.register(Shipping)
admin.site.register(Payment)
admin.site.register(Order)

