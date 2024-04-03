import json

from specs.models import SpecTask, SpecTaskRequest, Product
from specs.parsers.wildberries import dataparser
from specs.serializer import ProductServiceSerializer


class RequestDataService:
    @staticmethod
    def get_data_from_request(data: str) -> dict:
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            raise Exception('JSON is not valid')
        except Exception as e:
            raise Exception(str(e))
        if 'site_products' not in data:
            raise Exception('"site_products" key is required')
        if not isinstance(data['site_products'], list):
            raise Exception('"site_products" must be a list')
        if len(data['site_products']) == 0:
            raise Exception('"site_products" list cannot be empty')
        if not all(isinstance(item, str) for item in data['site_products']):
            raise Exception('Each item in "site_products" must be a string')
        if 'domain' not in data:
            raise Exception('"domain" key is required')
        if not isinstance(data['domain'], str):
            raise Exception('"domain" must be a str')
        if data['domain'] != 'wildberries.ru':
            raise Exception('"domain" str must be "wildberries.ru"')
        return data


class ProductService:
    @classmethod
    def create_products(cls, task_id: int):
        task = SpecTask.objects.get(id = task_id)
        site_products = SpecTaskRequest.objects.get(spec_task = task).data['site_products']
        domain = SpecTaskRequest.objects.get(spec_task = task).data['domain']

        for site_product in site_products:
            Product.objects.create(domain = domain, spec_task = task, data = {"site_product": site_product})

    @classmethod
    def send_products_to_parser(cls, task_id: int) -> None:
        products = Product.objects.filter(status = 'PARSING', spec_task__id = task_id)
        serialized_products = ProductServiceSerializer(products, many = True).data

        task = SpecTask.objects.get(id = task_id)
        task.task_status = 'PARSING'
        task.save()

        for serialized_data in serialized_products:
            dataparser(serialized_data['id'], serialized_data['data']['site_product'])
