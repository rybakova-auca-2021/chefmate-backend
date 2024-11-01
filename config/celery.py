from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

app.config_from_object('django.conf:settings', namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'change-status-every-day-at-10am': {
        'task': 'notification.tasks.send_notification',
        'schedule': crontab(hour=10, minute=0)
    },
}
