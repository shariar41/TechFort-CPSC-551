from django.shortcuts import render
from django.views.generic import ListView, DetailView


# Create your views here.


def blogs(request):
    return render(request, 'blog/blog_page.html')


def blog_details(request):
    return render(request, 'blog/blog_details.html')

