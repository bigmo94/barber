from celery import shared_task

from customers.utils import send_message


@shared_task
def send_verification_code_task(user_phone, verification_code):
    send_message({'receptor': user_phone, 'message': verification_code})
