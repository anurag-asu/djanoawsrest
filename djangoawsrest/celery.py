import os

from celery import Celery
from celery.schedules import crontab


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoawsrest.settings')

app = Celery('djangoawsrest', include=['celery_example.tasks'])

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'run_every_five_min': {
        'task': 'celery_example.tasks.run_every_5_min',
        'schedule': 120.0
    }
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
