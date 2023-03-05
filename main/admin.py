from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User, Plugin, LegalUser, PhysicalUser, Client


class LegalUserAdmin(admin.StackedInline):
    model = LegalUser
    list_display = list(map(lambda x: x.name, LegalUser._meta.get_fields()))


class PhysicalUserAdmin(admin.StackedInline):
    model = PhysicalUser
    list_display = list(map(lambda x: x.name, PhysicalUser._meta.get_fields()))


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ("email", "is_staff", "is_active", "date_joined")
    list_filter = ("email", "is_staff", "is_active", "date_joined")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
         ),
    )
    inlines = [LegalUserAdmin,
               PhysicalUserAdmin
               ]

    search_fields = ("email",)
    ordering = ("email",)


@admin.register(Plugin)
class PluginAdmin(admin.ModelAdmin):
    list_display = list(map(lambda x: x.name, Plugin._meta.get_fields()))


@admin.register(Client)
class PluginAdmin(admin.ModelAdmin):
    list_display = list(map(lambda x: x.name, Client._meta.get_fields()))
