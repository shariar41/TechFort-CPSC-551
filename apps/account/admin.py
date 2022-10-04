from django.contrib import admin
from .models import User, Profile

# Register your models here.
# email: demo@gmail.com pass: demo


class ProfileAdmin(admin.StackedInline):
    model = Profile


@admin.register(User)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProfileAdmin]

    class Meta:
        model = User


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass



# admin.site.register(User)
# admin.site.register(Profile)
# Register your models here.
