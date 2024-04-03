from __future__ import absolute_import
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parsing_api.settings')

app = Celery("parsing_api")
app.config_from_object('django.conf:settings', namespace='CELERY')

rabbitmq_user = os.getenv('RABBITMQ_USER')
rabbitmq_pass = os.getenv('RABBITMQ_PASS')
rabbitmq_host = os.getenv('RABBITMQ_HOST')
rabbitmq_port = os.getenv('RABBITMQ_PORT')

app.conf.broker_url = f'amqp://{rabbitmq_user}:{rabbitmq_pass}@{rabbitmq_host}:{rabbitmq_port}/'
app.conf.result_backend = 'rpc://'
app.autodiscover_tasks()