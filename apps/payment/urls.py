from django.urls import path
from . import views
from .views import CheckoutView  # , payment

app_name = 'payment'

urlpatterns = [
    # path('checkout/', views.checkout, name="checkout"),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    # path('payment/', views.payment, name="payment"),
    path('payment-completed/', views.complete_payment_page, name="payment-completed"),
    path('payment/<val_id>/<tran_id>', views.purchase, name="purchase"),
]
