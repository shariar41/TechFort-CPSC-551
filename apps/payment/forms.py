from django import forms
from .models import BillingAddress, CountryList

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# forms

class BillingForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=CountryList.objects.all(), empty_label=None, label="Country")

    class Meta:
        model = BillingAddress
        fields = ('email', 'address', 'city', 'country')

        widgets = {
            'email': forms.EmailInput(
                attrs={'class': "form-control", 'id': "email_address", 'required': ''}),
            'address': forms.TextInput(
                attrs={'class': "form-control", 'id': "p_address", 'required': ''}),
            # 'country': {'country': CountrySelect(
            #     attrs={'class': "form-control nice-select", 'id': 'country_name',
            #            'required': '', 'name': 'country_id'})},
            'city': forms.TextInput(
                attrs={'class': "form-control", 'id': "city_name", 'required': ''}),
        }
