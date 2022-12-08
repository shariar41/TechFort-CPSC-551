from django.contrib import admin

from apps.blog.models import Article, Blog, ArticleTag, ArticlePost

# Register your models here.

admin.site.register(Blog)
admin.site.register(Article)
admin.site.register(ArticleTag)
admin.site.register(ArticlePost)