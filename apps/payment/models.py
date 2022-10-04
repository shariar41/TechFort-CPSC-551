from django.conf import settings
from django.db import models


class CountryList(models.Model):
    name = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return self.name

    def is_fully_filled(self):
        field_names = [f.name for f in self._meta.get_fields()]

        for field_name in field_names:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True

    class Meta:
        verbose_name_plural = "Countries List"


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=264, blank=True)
    city = models.CharField(max_length=30, blank=True)
    country = models.OneToOneField(CountryList, on_delete=models.CASCADE, default="1")
    email = models.EmailField(unique=True, null=False)

    def __str__(self):
        return f"{self.user.first_name}'s billing address"

    def is_fully_filled(self):
        field_names = [f.name for f in self._meta.get_fields()]

        for field_name in field_names:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True

    class Meta:
        verbose_name_plural = "Billing Addresses"
