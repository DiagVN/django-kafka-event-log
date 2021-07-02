import os
from celery import Celery
from django.conf import settings
import rollbar
from celery.signals import task_failure

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')


app = Celery('root')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.LOCAL_APPS)


def celery_base_data_hook(request, data):
    data['framework'] = 'celery'


if os.environ.get('MODE') == 'worker':
    rollbar.init(**settings.ROLLBAR)

    rollbar.BASE_DATA_HOOK = celery_base_data_hook

    @task_failure.connect
    def handle_task_failure(**kw):
        rollbar.report_exc_info(extra_data=kw)
