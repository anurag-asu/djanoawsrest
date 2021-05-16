from django.conf import settings

from twilio.rest import Client


def send_sms_util(message):
    message_to_broadcast = (message)
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    for recipient in settings.SMS_BROADCAST_TO_NUMBERS:
        if recipient:
            client.messages.create(to=recipient,
                                   from_=settings.TWILIO_NUMBER,
                                   body=message_to_broadcast)