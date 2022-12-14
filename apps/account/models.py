from django.db import models
# To Create a Custom User Model and Admin Panel

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy

# To automatically create one to one objects

from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class MyUserManager(BaseUserManager):
    """ A custom Manager to deal with emails as unique identifer """

    def _create_user(self, first_name, phone, email, password, **extra_fields):
        """ Creates and saves a user with a given email and password"""
        if not email or not first_name or not phone:
            raise ValueError("All the fields must be set!")
        email = self.normalize_email(email)
        first_name = self.normalize_email(first_name)
        phone = self.normalize_email(phone)
        user = self.model(email=email, first_name=first_name, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, phone, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(first_name, phone, email, password, **extra_fields)


# class URole(models.Model):
#     ROLE_CHOICES = (
#         (1, "admin"),
#         (2, "customer"),
#         (3, "seller"))
#     role_id = models.AutoField(db_column='role_id', primary_key=True)
#     role_type = models.CharField(db_column='role_type', choices=ROLE_CHOICES, default=2)
#     role_desc = models.CharField(max_length=50, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'U_Role'


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('1', "admin"),
        ('2', "customer"),
        ('3', "seller"),)
    # user_id = models.AutoField(primary_key=True, default=1000)
    email = models.EmailField(unique=True, null=False)
    first_name = models.CharField(max_length=264, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    # role_type = models.CharField(max_length=1, db_column='role_type', choices=ROLE_CHOICES, default='2')
    is_staff = models.BooleanField(
        gettext_lazy('staff status'),
        default=False,
        help_text=gettext_lazy('Designates whether the user can log in this site')
    )
    is_seller = models.BooleanField(
        gettext_lazy('seller status'),
        default=False,
        help_text=gettext_lazy('Designates whether the user is a seller or not')
    )

    is_active = models.BooleanField(
        gettext_lazy('active'),
        default=True,
        help_text=gettext_lazy(
            'Designates whether this user should be treated as active. Unselect this instead of deleting accounts')
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'phone']
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    # def get_short_name(self):
    #     return self.last_name
    class Meta:
        db_table = 'User'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    lastname = models.CharField(max_length=264, blank=True)
    address_1 = models.TextField(max_length=300, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    apartment = models.CharField(max_length=20, blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=40, blank=True, null=True)
    profile_pic = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    store_desc = models.CharField(max_length=200, blank=True, null=True)
    hotline = models.CharField(max_length=11, blank=True, null=True)

    def __str__(self):
        return self.user.email + "'s Profile"

    def is_fully_filled(self):
        fields_names = [f.name for f in self._meta.get_fields()]

        for field_name in fields_names:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True

    class Meta:
        db_table = 'Profile'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
