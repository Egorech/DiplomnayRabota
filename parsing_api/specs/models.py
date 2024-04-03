from django.db import models

from users.models import CustomUser


class SpecTaskRequest(models.Model):
    data = models.JSONField(default=dict)
    spec_task = models.ForeignKey('SpecTask', on_delete=models.CASCADE, related_name='spec_task')

    class Meta:
        ordering = ['id']
        db_table = 'specs_spec_task_requests'


class SpecTask(models.Model):
    TASK_STATUS_CHOICES = (
        ("WAITING_DATA_PROCESSING", "waiting_data_processing"),
        ("DATA_PROCESSING", "data_processing"),
        ("WAITING_PARSING", "waiting_parsing"),
        ("PARSING", "parsing"),
        ("OK", "ok"),
        ("ERROR", "error"),
    )

    task_status = models.CharField(
        choices=TASK_STATUS_CHOICES,
        default='WAITING_DATA_PROCESSING',
        max_length=30,
    )
    user = models.ForeignKey(CustomUser, related_name='user_spec_tasks', on_delete=models.CASCADE, null = True)

    class Meta:
        ordering = ['id']
        db_table = 'specs_spec_tasks'


class Product(models.Model):
    STATUSES = {
        'PARSING': 'PARSING',
        'ERROR': 'ERROR',
        'OK': 'OK',
    }
    CHOICES = (
        (STATUSES['PARSING'], STATUSES['PARSING']),
        (STATUSES['ERROR'], STATUSES['ERROR']),
        (STATUSES['OK'], STATUSES['OK']),
    )
    spec_task = models.ForeignKey('SpecTask', related_name='spec_product', on_delete=models.CASCADE)
    domain = models.CharField(max_length=1000)
    data = models.JSONField(default=dict)
    status = models.CharField(max_length = 30, default = STATUSES['PARSING'], choices = CHOICES, db_index = True)

    class Meta:
        ordering = ['id']
        db_table = 'specs_products'
