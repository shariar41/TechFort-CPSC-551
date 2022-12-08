from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .models import Product, PCoverImage, Category
from django.db import connection

from ..order.models import Order


# from django.conf import settings
#### mysql query
# import mysql.connector as mydb
#
# conn = mydb.connect(host='127.0.0.1', port='3306', user='root',
#                     passwd='Saimon@0168', database='techfortlocalhost')
# cur = conn.cursor()


def home(request):
    print(connection.queries)
    if Product.objects.all():
        products = Product.objects.all()
    categories = Category.objects.all()
    # cur.execute("SELECT * FROM product")
    # productsList = list(cur.fetchall())
    # cur.execute("SELECT * FROM category")
    # categoriesList = list(cur.fetchall())
    # categories = []
    # for cat in categoriesList:
    #     categories.append(Category(cat[0], cat[1], cat[2]))
    context = {'categories': categories, 'products': products}
    return render(request, 'home.html', context)


def product_details(request, pk):
    product = Product.objects.get(productId=pk)
    # product = get_object_or_404(Product, id=pk)
    product_images = PCoverImage.objects.filter(productId=pk)
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
    p = Product.objects.filter(posted_user=request.user).select_related()
    # cont_rating_tmp = Order.objects.filter(
    #     created_by=request.user
    # ).aggregate(sum=sum('avg_rate'))
    print(p)

    if products and categories:
        # print(product_images[0].cover_image)
        if request.method == 'POST':
            catSelected = request.POST.get('catSelected')
            # products = Product.objects.get(category_id=catSelected)
            print(catSelected)
            # return render('products:shop', cat_id=catSelected)
            return HttpResponseRedirect(reverse("products:shopFilterProduct", kwargs={'cat_id': catSelected}))

        return render(request, 'products/shop_detail.html',
                      context={'products': products, 'categories': categories})
    return render(request, 'products/shop_detail.html',
                  context={'products': products, 'categories': categories})


def shopFilterProduct(request, cat_id):
    products = Product.objects.all()
    filteredproducts = Product.objects.filter(category=cat_id)
    categories = Category.objects.all()
    print(products)
    # if products and categories:
    #     # print(product_images[0].cover_image)
    #     return render(request, 'products/shop_detail.html',
    #                   context={'products': products, 'categories': categories})
    return render(request, 'products/shop_detail.html',
                  context={'products': products, 'filteredproducts': filteredproducts, 'categories': categories})


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
