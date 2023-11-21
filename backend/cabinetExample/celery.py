import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cabinetExample.settings')
app = Celery('cabinetExample')
app.config_from_object('django.conf:settings', namespace='CELERY')

# https://docs.celeryq.dev/en/stable/userguide/configuration.htm
app.conf.update(
    result_expires=60 * 60 * 24,  # Seconds after task stored to remove from DB
    task_routes={
        'app.tasks.update_rx_status': {'queue': 'rx-update'},
    },
)


# Load task modules from all registered Django apps.
app.autodiscover_tasks()
