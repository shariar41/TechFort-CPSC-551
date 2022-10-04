from django import template

# from ..models import Category
from ...products.models import Category

register = template.Library()


@register.filter
def categories_list():
    categories = Category.objects.all()[:10]
    print(categories[0])
    if categories.exists():
        categories = categories[0]
    else:
        categories = 0
    return {'categories': categories}
