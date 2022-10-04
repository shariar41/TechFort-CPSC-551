from django.urls import path
from . import views

urlpatterns = [
    path('view/', views.view_cart, name="view_cart"),
    path('add/<pk>/', views.add_to_cart, name="add_to_cart"),
    path('remove/<pk>/', views.remove_cart_item, name="remove"),
    path('increase/<pk>/', views.increase_cart, name="increase"),
    path('decrease/<pk>/', views.decrease_cart, name="decrease"),
]
