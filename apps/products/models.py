from django.db import models

from apps.account.models import User


# from models import Users


# Create your models here.


class Tag(models.Model):
    tag_name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.tag_name

    class Meta:
        db_table = 'ProductTag'


# class SubCategory(models.Model):
#     sub_category_name = models.CharField(max_length=30, blank=True)
#
#     def __str__(self):
#         return self.sub_category_name
#
#     class Meta:
#         verbose_name_plural = "Sub-categories"


class Category(models.Model):
    # sub_category = models.ManyToManyField(SubCategory, blank=True)
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=40, blank=True, null=True)
    category_description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "Categories"
        db_table = 'CATEGORY'


class Product(models.Model):
    productId = models.AutoField(db_column='productId', primary_key=True)  # Field name made lowercase.
    posted_user = models.ForeignKey(User, models.DO_NOTHING, db_column='posted_user')
    name = models.CharField(max_length=300, blank=True)
    image = models.CharField(unique=True, max_length=200, blank=True,
                             null=True)  # models.ImageField(upload_to='Products_Images/', null=True, blank=True)
    # image = models.ForeignKey(ProductImage, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tag')
    description = models.TextField(max_length=400, blank=True)
    old_price = models.FloatField(default=0.0, verbose_name="Old Price")
    new_price = models.FloatField(default=0.0, verbose_name="New Price")
    discount = models.FloatField(default=0.0)
    is_featured = models.BooleanField(default=False)
    is_offered = models.BooleanField(default=False)
    brand = models.CharField(max_length=264, blank=True)
    code = models.CharField(max_length=30, blank=True)
    availability = models.BooleanField(default=None, verbose_name="availability")
    color = models.CharField(max_length=30, blank=True)
    stock = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Product'


# class ProductImage(models.Model):
#     name = models.CharField(max_length=255)
#     product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
#     cover_image = models.ImageField(upload_to='Products_Images/', null=True, blank=True)
#
#     def __str__(self):
#         return self.name


class PCoverImage(models.Model):
    image_link = models.CharField(unique=True, max_length=200, blank=True, null=True)
    productId = models.ForeignKey(Product, models.CASCADE, db_column='productId')  # Field name made lowercase.
    alt = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return self.image_link

    class Meta:
        db_table = 'P_COVER_IMAGE'
