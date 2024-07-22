from django.core.mail import send_mail
from django.conf import settings
import time


def send_email_to_clients():
    subject = 'This is GTA 5'
    message = 'This is test'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ["aryansukhadia2511@gmail.com"]
    send_mail(subject, message,from_email, recipient_list)
