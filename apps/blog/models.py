from django.db import models

from apps.account.models import User


# Create your models here.


class Blog(models.Model):
    blog_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    blog_image = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.title
    class Meta:
        db_table = 'BLOG'


class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    a_blog = models.ForeignKey(Blog, models.CASCADE, blank=False, null=False)
    authur = models.ForeignKey(User, models.PROTECT, db_column='authur')
    a_title = models.CharField(max_length=100, blank=True, null=True)
    article_content = models.TextField(blank=True, null=True)
    article_photo = models.CharField(max_length=500, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.a_title
    class Meta:
        db_table = 'ARTICLE'


class ArticleTag(models.Model):
    article = models.OneToOneField(Article, models.DO_NOTHING, primary_key=True)
    tag_name = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        db_table = 'ArticleTag'


class ArticlePost(models.Model):
    p_post_id = models.AutoField(primary_key=True)
    posted_by = models.ForeignKey(User, models.PROTECT, db_column='posted_by')
    p_article = models.ForeignKey(Article, models.CASCADE)
    date_posted = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'POST'
