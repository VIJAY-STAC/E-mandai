from __future__ import absolute_import, unicode_literals
from celery.utils.log import get_task_logger
from django.core.mail import EmailMessage
import os
from celery import shared_task
from users.utils import send_email

logger = get_task_logger(__name__)

@shared_task
def add(a,b):
    return a + b

@shared_task
def send_email(data):
    email = EmailMessage(
        subject=data['subject'],
        body=data['body'],
        from_email=os.environ.get('HOST_USER'),
        to =[data['to_email']]
    )
    print('from_email')
    email.send( )
    print('from_email')
    return "mail sent"