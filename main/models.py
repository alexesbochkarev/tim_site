from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models

from main.managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Plugin(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, help_text="User provided name for plugin")
    document_count = models.IntegerField(default=0, help_text="Number of documents filled with plugin")
    unique_users_attracted = models.IntegerField(default=0, help_text="Number of attracted unique users")
    plugin_id = models.UUIDField(unique=True, help_text="Unique id for plugin")
    plugin_secret = models.UUIDField(help_text="Secret used verify plugin")
    valid_until_date = models.DateField(help_text="Plugin valid until this date")


class Client(models.Model):
    uuid = models.UUIDField(primary_key=True, unique=True, help_text="Unique id for clients")
    phone_number = models.CharField(unique=True, max_length=11)
    code = models.CharField(default="0000", unique=True, max_length=4)
    is_used = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True, help_text="Date client joined")
    code_date_send = models.DateTimeField(auto_now_add=True, help_text="Date code send to client")


class PhysicalUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)


class LegalUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)

    organization_type = models.CharField(max_length=200)
    organization_name = models.CharField(max_length=200)
    organization_address = models.CharField(max_length=200)

    INN = models.CharField(max_length=12)
    KPP = models.CharField(max_length=9)
