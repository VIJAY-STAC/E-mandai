from __future__ import absolute_import, unicode_literals

from argparse import Namespace

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mandai.settings')

app = Celery('Mandai')

app.config_from_object('django.conf:settings', namespace='CELLERY')

app.autodiscover_tasks()