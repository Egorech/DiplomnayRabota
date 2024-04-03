from parsing_api.celery import *

from specs.models import SpecTask
from specs.services import ProductService


@app.task(queue='specs_request_data_handler_queue')
def handle_products(task_id: int) -> None:
    task = SpecTask.objects.get(id=task_id)
    task.task_status = 'DATA_PROCESSING'
    task.save()

    ProductService.create_products(task_id)
    task.task_status = 'WAITING_PARSING'
    task.save()

    ProductService.send_products_to_parser(task_id)
