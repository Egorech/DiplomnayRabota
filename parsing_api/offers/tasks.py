from parsing_api.celery import *
from offers.models import *
from offers.services import ProductService
import time


@app.task(queue = 'offers_request_data_handler_queue')
def handle_products(task_id: int) -> None:
    task = OfferTask.objects.get(id = task_id)

    task.task_status = 'DATA_PROCESSING'
    task.save()
    ProductService.create_products(task.id)
    # time.sleep(100)

    task.task_status = 'WAITING_PARSING'
    task.save()
    ProductService.send_products_to_parser(task_id)
