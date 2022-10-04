from django.contrib import admin

# Register your models here.
from .models import CountryList, BillingAddress

admin.site.register(BillingAddress)
admin.site.register(CountryList)
