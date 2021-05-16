from django.http import HttpResponse
from django.conf import settings
from celery_example.tasks import sleepy

from twilio.rest import Client

# Create your views here.


def index(request):
    sleepy.delay()
    return HttpResponse('Here!')


def send_sms(request):
    from celery_example.utils import send_sms_util
    send_sms_util("Test")
    return HttpResponse("messages sent!", 200)


def get_cowin_response(request):
    from celery_example.tasks import run_every_5_min
    return run_every_5_min()
