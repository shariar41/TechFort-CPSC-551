from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
     path('blogs/', views.blogs, name='blogs'),
     path('blogs_details/', views.blog_details, name='blogs_details'),
]