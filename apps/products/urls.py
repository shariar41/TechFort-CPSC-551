from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.shop, name='home'),#views.home
    # path('home/', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('shop/<cat_id>', views.shopFilterProduct, name='shopFilterProduct'),
    # path('shop/category-id=<int:id>', views.Shop_Filter.as_view(), name='shop-filter'),
    path('product/<pk>', views.product_details, name='productDetails'),
    # path('wishlist/', views.WishList.as_view(), name='wishlist'),
    # path('compare/', views.ProductCompare.as_view(), name='compare'),
    # path('checkout/', views.CheckOut.as_view(), name='checkout'),
    path('contact/', views.contact_page, name='contact'),

]
