import time

import requests
import json

from tim_site.settings import CODE_MASTER_KEY

# host = "http://192.168.0.109/"
host = "https://time-money.shop/"


def send_code(phone: str):
    r = requests.post(f"{host}code/send",
                      data={'phone_number': phone, 'master_key': CODE_MASTER_KEY})

    print(len(phone))

    print(r.status_code, r.reason)
    print(r.text)


def check_code(phone: str, code: str):
    r = requests.post(f"{host}code/check",
                      data={'phone_number': phone, 'master_key': CODE_MASTER_KEY, 'code': code})

    print(r.status_code, r.reason)
    print(r.text)


phone_num = "8 983 523 46 87"
send_code(phone_num)
check_code(phone_num, input().strip())
