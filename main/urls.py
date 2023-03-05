from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views
from .forms import UserLoginForm, PasswordResetForm, SetPasswordForm

urlpatterns = [
    path("", views.index, name="home"),

    # path("", include("django.contrib.auth.urls")),
    path("login", auth_views.LoginView.as_view(redirect_authenticated_user=True, authentication_form=UserLoginForm, ),
         name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("password_reset/", auth_views.PasswordResetView.as_view(form_class=PasswordResetForm), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done", ),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(form_class=SetPasswordForm),
         name="password_reset_confirm", ),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete", ),

    path("register", views.register, name="register"),
    path("register/legal", views.register_legal, name="register_legal"),
    path("register/physical", views.register_physical, name="register_physical"),

    path("download", views.download, name="download"),
    path("privacy_mobile", views.privacy_mobile, name="privacy_mobile"),
    path("privacy_plugin", views.privacy_plugin, name="privacy_plugin"),

    path("personal_cabinet", views.personal_cabinet, name="personal_cabinet"),
    path("personal_cabinet/add", views.personal_cabinet_add, name="personal_cabinet_add"),

    path("personal_cabinet/download_qrcode/<uuid:cur_uuid>", views.download_qr_code, name="download_qrcode"),
    path("personal_cabinet/renew/<uuid:cur_uuid>", views.renew_plugin, name="renew_plugin"),

    path("code/send", views.code_send),
    path("code/check", views.code_check),

    path("redirect", views.redirect_mobile),
]
