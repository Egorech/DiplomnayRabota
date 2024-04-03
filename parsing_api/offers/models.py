from django.db import models

from users.models import CustomUser


class OfferTaskRequest(models.Model):
    data = models.JSONField(default=dict)
    offer_task = models.ForeignKey('OfferTask', on_delete=models.CASCADE, related_name='offer_task')

    class Meta:
        ordering = ['id']
        db_table = 'offers_offer_task_requests'


class OfferTask(models.Model):
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
    user = models.ForeignKey(CustomUser, related_name='user_offer_tasks', on_delete=models.CASCADE, null = True)

    class Meta:
        ordering = ['id']
        db_table = 'offers_offer_tasks'


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
    offer_task = models.ForeignKey('OfferTask', related_name='product', on_delete=models.CASCADE)
    region = models.IntegerField(default=77)
    domain = models.CharField(max_length=200)
    link = models.CharField(max_length=1000)
    status = models.CharField(max_length=30, default=STATUSES['PARSING'], choices=CHOICES, db_index=True)
    data = models.JSONField(default=dict)

    class Meta:
        ordering = ['id']
        db_table = 'offers_products'


class Offer(models.Model):
    product = models.ForeignKey('Product', related_name='offers', on_delete=models.CASCADE)
    data = models.JSONField(default=dict)

    class Meta:
        ordering = ['id']
        db_table = 'offers_offers'
