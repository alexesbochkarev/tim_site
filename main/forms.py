import datetime
import uuid

import django.contrib.auth.forms as default_forms
import django.forms as forms
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import User, PhysicalUser, LegalUser, Plugin

_nice_look_attrs = {"class": "form-control", "placeholder": "1"}
_nice_look_widget = forms.TextInput(attrs=_nice_look_attrs)
_template_name = "form.html"


def get_email_field(label: str):
    return forms.EmailField(label=label, required=True, widget=forms.EmailInput(attrs=_nice_look_attrs))


def get_password_field(label: str):
    return forms.CharField(
        label=label,
        strip=False,
        widget=forms.PasswordInput(attrs=_nice_look_attrs | {"autocomplete": "current-password"}),

    )


def get_name_field(label: str):
    return forms.CharField(label=label, strip=True, max_length=100, widget=_nice_look_widget)


def get_organization_field(label: str):
    return forms.CharField(label=label, strip=True, max_length=200, widget=_nice_look_widget)


def get_meta_organization_field(label: str):
    return forms.IntegerField(label=label, min_value=0, max_value=999999999999,
                              widget=forms.NumberInput(_nice_look_attrs | {
                                  "min": "0", "max": "999999999999"
                              }))


class UserChangeForm(default_forms.UserChangeForm):
    """Form for admin view"""

    class Meta:
        model = User
        fields = ("email",)
        field_classes = {"username": forms.EmailField}


class UserCreationForm(default_forms.UserCreationForm):
    """Common things for user creation"""

    email = get_email_field("Email")
    email1 = get_email_field("Подтвердите Email")

    password1 = get_password_field("Пароль")
    password2 = get_password_field("Повторите пароль")

    last_name = get_name_field("Имя")
    first_name = get_name_field("Фамилия")
    patronymic = get_name_field("Отчество")

    def clean_email(self):
        return self.cleaned_data["email"].lower()

    def clean_email1(self):
        email = self.cleaned_data["email"]
        email1 = self.cleaned_data["email1"]
        if email and email1 and email != email1:
            raise ValidationError("Enter the same email as before, for verification")

        return email1


class PhysicalUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True,
                             widget=forms.EmailInput(attrs=_nice_look_attrs | {"id": "email_id-1"}))
    email1 = forms.EmailField(label="Подтвердите email", required=True,
                              widget=forms.EmailInput(attrs=_nice_look_attrs | {"id": "email_id-2"}))

    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs=_nice_look_attrs | {"autocomplete": "current-password", "id": "pass_id-1"}))
    password2 = forms.CharField(
        label="Повторите пароль",
        strip=False,
        widget=forms.PasswordInput(attrs=_nice_look_attrs | {"autocomplete": "current-password", "id": "pass_id-2"}))

    class Meta:
        model = User
        fields = ("email", "email1", "password1", "password2", "first_name", "last_name", "patronymic")

    @transaction.atomic
    def save(self, commit=True):
        user = super(PhysicalUserRegistrationForm, self).save(commit=True)
        PhysicalUser.objects.create(user=user,
                                    first_name=self.cleaned_data["first_name"],
                                    last_name=self.cleaned_data["last_name"],
                                    patronymic=self.cleaned_data["patronymic"],
                                    )
        return user


class LegalUserRegistrationForm(UserCreationForm):
    organization_type = get_organization_field("Тип организации")
    organization_name = get_organization_field("Название организации")
    organization_address = get_organization_field("Адрес организации")

    INN = get_meta_organization_field("ИНН")
    KPP = get_meta_organization_field("КПП")

    class Meta:
        model = User
        fields = ("email", "email1", "password1", "password2", "first_name", "last_name", "patronymic")

    @transaction.atomic
    def save(self, commit=True):
        user = super(LegalUserRegistrationForm, self).save(commit=True)
        LegalUser.objects.create(user=user,
                                 first_name=self.cleaned_data["first_name"],
                                 last_name=self.cleaned_data["last_name"],
                                 patronymic=self.cleaned_data["patronymic"],
                                 organization_type=self.cleaned_data["organization_type"],
                                 organization_name=self.cleaned_data["organization_name"],
                                 organization_address=self.cleaned_data["organization_address"],
                                 INN=self.cleaned_data["INN"],
                                 KPP=self.cleaned_data["KPP"],
                                 )
        return user


class UserLoginForm(default_forms.AuthenticationForm):
    template_name = _template_name

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(widget=forms.TextInput(
        attrs=_nice_look_attrs | {"autofocus": True, "autocapitalize": "none", "autocomplete": "username",
                                  "placeholder": "Email"}))
    password = get_password_field("Password")


class PasswordResetForm(default_forms.PasswordResetForm):

    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs=_nice_look_attrs))


class SetPasswordForm(default_forms.SetPasswordForm):
    template_name = _template_name
    new_password1 = get_password_field("Новый пароль")
    new_password2 = get_password_field("Повторите новый пароль")


class AddPluginForm(forms.Form):
    name = forms.CharField(strip=True, max_length=200, widget=_nice_look_widget)

    class Meta:
        model = Plugin
        fields = ("name",)

    def save(self, user):
        plugin = Plugin.objects.create(user=user,
                                       name=self.cleaned_data["name"],
                                       plugin_id=uuid.uuid4(),
                                       plugin_secret=uuid.uuid4(),
                                       valid_until_date=datetime.date.today()
                                       )
        return plugin
