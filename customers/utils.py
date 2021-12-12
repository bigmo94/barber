import random

from rest_framework.exceptions import ValidationError
from django.utils import timezone
from kavenegar import KavenegarAPI, APIException, HTTPException


def code_generator():
    return random.randint(10000, 99999)


def validate_birthday(value):
    if value > timezone.now().date():
        raise ValidationError('birthday field is not valid')
    return value


def send_message(data):
    body = data.get('message')
    receptor = data.get('receptor')
    try:
        api = KavenegarAPI(
            '674E5A306D6133654A4D7361764737413032524C6B5467524F714976386C4E664F5371776E3049515173553D')
        params = {
            'sender': '1000596446',
            'receptor': receptor,
            'message': "Your verify code is: {}".format(body),
        }
        api.sms_send(params)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
