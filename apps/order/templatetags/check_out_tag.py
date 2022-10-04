from django import template

from ..models import Order, Cart

register = template.Library()


# @register.filter
# def find_remainder(num):
#     if num:
#         return num % 2
#     else:
#         return 0
