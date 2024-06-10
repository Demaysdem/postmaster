import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'post_master.settings')

app = Celery('post_master')

app.conf.broker_connection_retry_on_startup = True


app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'every_minute': {
        'task': 'publication.tasks.check_message_status',
        'schedule': crontab(minute='*/1'),

    }
}

app.autodiscover_tasks()
