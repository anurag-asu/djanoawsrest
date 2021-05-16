import pytz
import requests

from time import sleep
from datetime import datetime

from celery import shared_task
from django.http import JsonResponse

from djangoawsrest.celery import app


@shared_task
def sleepy():
    sleep(10)
    return None


@app.task
def run_every_5_min():
    try:
        ist = pytz.timezone('Asia/Calcutta')
        date = datetime.now(ist)
        date = str(date.day) + '-' + str(date.month) + '-' + str(date.year)

        headers = {
            'Host': 'cdn-api.co-vin.in',
            'TE': 'Trailers',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0',
            'X-user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 FKUA/website/41/website/Desktop',
            'Accept': 'application/json, text/plain, */*',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'DNT': '1',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJlOGZjNjY0OC0wMGQyLTQ2ZWItYjJlNS02YTZjZGZiMjYxMDUiLCJ1c2VyX2lkIjoiZThmYzY2NDgtMDBkMi00NmViLWIyZTUtNmE2Y2RmYjI2MTA1IiwidXNlcl90eXBlIjoiQkVORUZJQ0lBUlkiLCJtb2JpbGVfbnVtYmVyIjo5OTUzNzIyMzk2LCJiZW5lZmljaWFyeV9yZWZlcmVuY2VfaWQiOjk0NTIyNDY2OTQxNjcwLCJzZWNyZXRfa2V5IjoiYjVjYWIxNjctNzk3Ny00ZGYxLTgwMjctYTYzYWExNDRmMDRlIiwidWEiOiJNb3ppbGxhLzUuMCAoTWFjaW50b3NoOyBJbnRlbCBNYWMgT1MgWCAxMC4xNTsgcnY6ODguMCkgR2Vja28vMjAxMDAxMDEgRmlyZWZveC84OC4wIiwiZGF0ZV9tb2RpZmllZCI6IjIwMjEtMDUtMTVUMDY6NDc6MDEuMzY0WiIsImlhdCI6MTYyMTA2MTIyMSwiZXhwIjoxNjIxMDYyMTIxfQ.oQ4KpWcCj26Ziz_jdNlKrAe72foagL8Zt0z_mMwUShs'
        }

        url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByPin?pincode=246149&date={}".format(date)

        res = requests.get(url, headers=headers)

        res.raise_for_status()

        centers = res.json().get('centers')

        for center in centers:
            sessions = center.get('sessions')
            for session in sessions:
                if session.get('available_capacity') > 0 and session.get('min_age_limit') >= 18:
                    from celery_example.utils import send_sms_util
                    send_sms_util("Vaccines available for your pincode")

        return JsonResponse(res.json(), status=200)
    except Exception as e:
        print('[run_every_5_min] error {}'.format(e))
        return JsonResponse({"error": "something went wrong"}, status=500)
