from django.db import models


# Create your models here.


class Tag(models.Model):
    tag_name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.tag_name


class SubCategory(models.Model):
    sub_category_name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.sub_category_name

    class Meta:
        verbose_name_plural = "Sub-categories"


class Category(models.Model):
    category_name = models.CharField(max_length=30, blank=True)
    sub_category = models.ManyToManyField(SubCategory, blank=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='Products_Images/', null=True, blank=True)
    # image = models.ForeignKey(ProductImage, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tag')
    description = models.TextField(max_length=400, blank=True)
    old_price = models.FloatField(default=0.0, verbose_name="Old Price")
    new_price = models.FloatField(default=0.0, verbose_name="New Price")
    discount = models.FloatField(default=0.0)
    brand = models.CharField(max_length=264, blank=True)
    code = models.CharField(max_length=30, blank=True)
    availability = models.BooleanField(default=None, verbose_name="Quantity")
    color = models.CharField(max_length=30, blank=True)
    quantity = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to='Products_Images/', null=True, blank=True)

    def __str__(self):
        return self.name
