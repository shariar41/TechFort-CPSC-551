from django.contrib import admin

# Register your models here.
from .models import Product, Category, Tag, PCoverImage  # , ProductImage, SubCategory

admin.site.register(Category)
# admin.site.register(SubCategory)
admin.site.register(Tag)


class ProductImageAdmin(admin.StackedInline):
    model = PCoverImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]

    class Meta:
        model = Product


@admin.register(PCoverImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass

# admin.site.register(Product, ProductAdmin)

# admin.site.register(ProductImage)
