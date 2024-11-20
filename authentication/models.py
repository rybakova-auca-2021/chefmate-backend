from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.contrib.auth.models import PermissionsMixin
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, unique=True, null=True)
    email = models.EmailField(max_length=255, unique=True, null=True)
    password = models.CharField(max_length=100, null=True)
    confirm_password = models.CharField(max_length=100, null=True)
    birth_date = models.DateField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_photo = models.URLField(blank=True, null=True)
    username = models.CharField(max_length=255, null=True)
    preferred_cuisines = models.ManyToManyField('preferences.Cuisine', blank=True, related_name='users')
    preferred_food = models.ManyToManyField('preferences.Food', blank=True, related_name='users')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.first_name or self.email


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.code


class Bonus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    def __str__(self):
        return f'Bonus of {self.user}: {self.amount}'


class Branch(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="flavorize/branch/", null=True)
    address = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        default=0,
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        default=0,
    )

    def __str__(self):
        return self.title
