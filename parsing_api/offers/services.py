import json
import logging
import re
from urllib.parse import urlparse

from offers.models import OfferTaskRequest, OfferTask, Product
from offers.repositories import ProductRepository
from offers.serializer import ProductServiceSerializer
from offers.parsers.wildberries import dataparser


class RequestDataService:
    @staticmethod
    def get_data_from_request(data: str) -> dict:
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            raise Exception('JSON is not valid')
        except Exception as e:
            raise Exception(str(e))
        if "links" not in data:
            raise Exception('links key is required')
        if not isinstance(data["links"], list):
            raise Exception('links must be a list')
        if len(data["links"]) == 0:
            raise Exception('links list cannot be empty')
        if not all(isinstance(item, str) for item in data["links"]):
            raise Exception('Each item in links must be a string')
        return data


class RegionService:
    DEFAULT_REGION = 77

    @classmethod
    def get_regions_from_data(cls, data: dict) -> dict:
        if 'regions' not in data or not data['regions']:
            data['regions'] = [77]
            return data
        if not isinstance(data['regions'], list):
            raise Exception('"regions" must be a list')
        if not all(isinstance(item, int) for item in data['regions']):
            raise Exception('Each item in "regions" must be a integer')
        return data


class UrlHandlerService:
    @classmethod
    def remove_www(cls, domain):
        pattern = r'^www\.(.*)$'  # Шаблон для поиска "www." в начале строки
        match = re.match(pattern, domain)
        if match:
            return match.group(1)
        else:
            return domain


class ProductService:
    @classmethod
    def create_products(cls, task_id: int):
        task = OfferTask.objects.get(id = task_id)
        data = OfferTaskRequest.objects.get(offer_task = task).data
        regions = data['regions']
        links = data['links']

        for region in regions:
            for link in links:
                try:
                    domain = UrlHandlerService.remove_www(urlparse(link).netloc)
                    pattern = r'/(\d+)/'  # https://www.wildberries.ru/catalog/173484907/detail.aspx -> 173484907
                    match = re.search(pattern, link)
                    if domain in ['wildberries.ru'] and match:
                        data = match.group(1)  # извлечение первого элемента
                        data = {'model_id': int(data)}
                        ProductRepository.create(region = region, domain = domain, link = link, offer_task = task, data = data)
                    else:
                        logger = logging.getLogger('handle_products')
                        logger.info(f'Вызвано исключение из-за неправильно указанного домена -> "{domain}"')
                        raise Exception
                except Exception:
                    ProductRepository.create(region = region, domain = domain, link = link, offer_task = task, status = 'ERROR')

    @classmethod
    def send_products_to_parser(cls, task_id: int) -> None:
        products = Product.objects.filter(status = 'PARSING', offer_task__id = task_id)
        serialized_products = ProductServiceSerializer(products, many = True).data

        task = OfferTask.objects.get(id = task_id)
        task.task_status = 'PARSING'
        task.save()

        for serialized_data in serialized_products:
            dataparser(serialized_data['id'], serialized_data['data']['model_id'])
