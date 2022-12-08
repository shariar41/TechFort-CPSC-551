from django.shortcuts import render
from django.views.generic import ListView, DetailView

from apps.blog.models import Blog, Article


# Create your views here.


def blogs(request):
    articles = Article.objects.all()
    # if articles:
    return render(request, 'blog/blog_page.html',
                  context={'articles': articles})


def blog_details(request):
    return render(request, 'blog/blog_details.html')


