from django.core.mail import EmailMessage
import os
from django.db import transaction, connections


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=os.environ.get('HOST_USER'),
            to =[data['to_email']]
        )
        email.send( )



def run_query(query, args=None):
    default_conn = connections['default']
    with default_conn.cursor() as cur:
        if args:
            cur.execute(query, args)
        else:
            cur.execute(query)
        return cur.fetchall()