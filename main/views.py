import datetime
import io
import json
import uuid

import requests
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render, redirect

import qrcode
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from qrcode.image.pure import PyPNGImage

from .forms import PhysicalUserRegistrationForm, LegalUserRegistrationForm, AddPluginForm
from .models import User, LegalUser, PhysicalUser, Plugin, Client
from .tables import PluginTable, PhysicalUserTable, LegalUserTable


# Create your views here.

def index(request):
    return render(request, "index.html")


@login_required
def download(request):
    return render(request, "download.html")


def privacy_mobile(request):
    return render(request, "privacy_mobile.html")


def privacy_plugin(request):
    return render(request, "privacy_plugin.html")


@user_passes_test(lambda user: user.is_anonymous, login_url=settings.LOGOUT_REDIRECT_URL)
def register(request):
    return render(request, "registration/register.html")


@user_passes_test(lambda user: user.is_anonymous, login_url=settings.LOGOUT_REDIRECT_URL)
def register_legal(request):
    form = LegalUserRegistrationForm()
    if request.method == "POST":
        form = LegalUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home", permanent=False)
    return render(request, "registration/login.html", context={"form": form})


@user_passes_test(lambda user: user.is_anonymous, login_url=settings.LOGOUT_REDIRECT_URL)
def register_physical(request):
    form = PhysicalUserRegistrationForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home", permanent=False)
    return render(request, "registration/login.html", context={"form": form})


@login_required
def personal_cabinet(request):
    if PhysicalUser.objects.filter(user=request.user).exists():
        user_table = PhysicalUserTable(PhysicalUser.objects.filter(user=request.user))
    elif LegalUser.objects.filter(user=request.user).exists():
        user_table = LegalUserTable(LegalUser.objects.filter(user=request.user))
    else:
        user_table = None

    plugins_table = PluginTable(Plugin.objects.filter(user=request.user))

    return render(request, "personal_cabinet.html",
                  context={"plugins_table": plugins_table.create_table(), "user_table": user_table})


@login_required
def personal_cabinet_add(request):
    form = AddPluginForm()
    if request.method == "POST":
        form = AddPluginForm(request.POST)
        if form.is_valid():
            form.save(request.user)
        return redirect("personal_cabinet", permanent=False)
    return render(request, "personal_cabinet_add_plugin.html", context={"form": form})


@login_required
def download_qr_code(request, cur_uuid: uuid.UUID):
    img = qrcode.make(settings.QRCODE_URL_SCHEME.format(cur_uuid),
                      box_size=10,
                      error_correction=qrcode.constants.ERROR_CORRECT_H,
                      image_factory=PyPNGImage,
                      )

    temp_file = io.BytesIO()
    img.save(temp_file)

    return HttpResponse(temp_file.getvalue(), content_type='image/png')


@login_required
def renew_plugin(request, cur_uuid: uuid.UUID):
    plugin = Plugin.objects.get(plugin_id=cur_uuid)
    plugin.valid_until_date += datetime.timedelta(days=1)
    plugin.save()
    return redirect("personal_cabinet", permanent=False)


def redirect_mobile(request):
    return render(request, "redirect_mobile.html")


def parse_phone_number(phone_number: str):
    number = "".join(filter(lambda x: x.isdigit(), phone_number.replace("+7", "8").replace("+", "")))
    if number.startswith("7"):
        number.replace("7", "8", 1)
    return number


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def send_code_to_phone(phone_number: str, ip: str):
    code, message = None, None
    r = requests.post(f"https://sms.ru/code/call",
                      data={'phone': phone_number, 'ip': ip, 'api_id': "72AB403C-AD9A-AE4B-443A-477A49704295"})
    if r.status_code == 200:
        answer = json.loads(r.text)
        if answer["status"] == "OK":
            code = int(answer["code"])
            if answer.get("free_send"):
                message = answer["Code reactivated"]
        else:
            message = answer["status_text"]
    else:
        message = "Bad response status code"
    return code, message


@require_POST
@csrf_exempt
def code_send(request):
    if request.POST.get("master_key", "") == settings.CODE_MASTER_KEY:
        phone_number = parse_phone_number(request.POST.get("phone_number", ""))
        if len(phone_number) == 11:
            if not Client.objects.filter(phone_number=phone_number).exists():
                Client.objects.create(uuid=uuid.uuid4(), phone_number=phone_number)
            code_and_message = send_code_to_phone(phone_number, get_client_ip(request))
            if code_and_message[0] is not None:
                client = Client.objects.get(phone_number=phone_number)
                client.code = code_and_message
                client.is_used = False
                client.save()
                data = {"message": "Code sent"}
            else:
                data = {"message": f"Failed to send code. Error message: {code_and_message}"}
        else:
            data = {"message": "Please supply valid 'phone_number'"}
    else:
        data = {"message": "Please supply valid 'master_key'"}
    return JsonResponse(data)


@require_POST
@csrf_exempt
def code_check(request):
    if request.POST.get("master_key", "") == settings.CODE_MASTER_KEY:
        phone_number = parse_phone_number(request.POST.get("phone_number", ""))
        if len(phone_number) == 11:
            if len(code := request.POST.get("code", "")) == 4 and code.isdigit():
                if Client.objects.filter(phone_number=phone_number).exists():
                    client = Client.objects.get(phone_number=phone_number)
                    if client.code == code:
                        if not client.is_used:
                            if client.code_date_send + settings.CODE_ALIVE_TIMEDELTA > \
                                    datetime.datetime.now(datetime.timezone.utc):
                                client.is_used = True
                                client.save()
                                data = {"message": "Success", "uuid": client.uuid}
                            else:
                                data = {"message": "Code expired"}
                        else:
                            data = {"message": "Code already used"}
                    else:
                        data = {"message": "Wrong code"}
                else:
                    data = {"message": "Client not registered yet"}
            else:
                data = {"message": "Please supply valid 'code'"}
        else:
            data = {"message": "Please supply valid 'phone_number'"}
    else:
        data = {"message": "Please supply valid 'master_key'"}
    return JsonResponse(data)
