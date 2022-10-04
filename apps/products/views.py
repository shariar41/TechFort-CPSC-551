from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

from .models import Product, ProductImage, Category


def home(request):
    categories = Category.objects.all()[:10]
    context = {'categories': categories}
    return render(request, 'home.html', context)


def product_details(request, pk):
    product = Product.objects.get(id=pk)
    # product = get_object_or_404(Product, id=pk)
    product_images = ProductImage.objects.filter(product_id=pk)
    if product:
        # print(product_images[0].cover_image)
        return render(request, 'products/Products_detail.html',
                      context={'product': product, 'product_images': product_images})
    return render(request, 'products/Products_detail.html')


# class ProductDetail(LoginRequiredMixin, DetailView):
#     model = Product
#     template_name = 'products/Products_detail.html'


# class Shop(ListView):
#     queryset = Product.objects.all()
#     models = Product
#     template_name = "products/shop_detail.html"


def shop(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    if products and categories:
        # print(product_images[0].cover_image)
        return render(request, 'products/shop_detail.html',
                      context={'products': products, 'categories': categories})
    return render(request, 'home.html')



class ShopFilter(ListView):
    # queryset = Product.objects.filter()
    models = Product
    template_name = "products/shop_detail.html"

    def get_queryset(self):
        return Product.objects.filter(self.request.resolver_match.kwargs['id'])


class ProductReact(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)


class WishList(ListView):
    model = Product
    template_name = "products/wish_list.html"


class ProductCompare(ListView):
    model = Product
    template_name = "products/product_compare.html"


def contact_page(request):
    return render(request, 'products/contact.html')
