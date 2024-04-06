import json

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from offers.models import *
from offers.tasks import handle_products


class OffersViewsTestCase(APITestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username = 'user1', email = 'user1@example.com', password = 'password1')
        self.user2 = CustomUser.objects.create_user(username = 'user2', email = 'user2@example.com', password = 'password2')
        self.client.force_login(self.user1)
        self.client2 = APIClient()  # Создание второго клиента
        self.client2.force_login(self.user2)

    def test_create_parsing_task_get_request(self):
        url = '/v1/offers/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_answer = {
            'Example  json request on parse data:': {
                'regions': [213, 2],
                'links': ['https://www.wildberries.ru/catalog/161607624/detail.aspx',
                          'https://www.wildberries.ru/catalog/143892937/detail.aspx']
            },
            'Possible statuses:': {
                'DATA_PROCESSING': 'обработка данных',
                'ERROR': 'ошибка',
                'OK': 'завершено',
                'PARSING ': 'данные в процессе парсинга',
                'WAITING_DATA_PROCESSING': 'ожидание обработки данных',
                'WAITING_PARSING ': 'ожидание парсинга'
            },
            'links field': 'list of links that will be used to parse data',
            'regions field': 'list of regions for which data will be parsed'
        }
        self.assertEqual(expected_answer, response.json())

    def test_create_parsing_task_post_request(self):
        url = '/v1/offers/'
        data = {
            "regions": [213],
            "links": ["https://www.wildberries.ru/catalog/161607624/detail.aspx"]
        }
        response = self.client.post(url, data = json.dumps(data), content_type = 'application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, response.json()['task_id'])
        self.assertEqual('http://localhost:8000/v1/offers/1/', response.json()['link for get answer'])

    def test_task_result_not_found_task_exception(self):
        url = '/v1/offers/10/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual({'detail': 'No such task_id'}, response.json())

    def test_task_result_permission_denied_exception(self):
        url = '/v1/offers/'
        data = {
            "regions": [213],
            "links": ["https://www.wildberries.ru/catalog/161607624/detail.aspx"]
        }
        response = self.client.post(url, data = json.dumps(data), content_type = 'application/json')
        url = f'/v1/offers/{response.json()["task_id"]}/'
        response = self.client2.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual({'detail': 'This task is not yours'}, response.json())

    def test_task_result_status_ok(self):
        url = '/v1/offers/'
        data = {
            "regions": [213],
            "links": ["https://www.wildberries.ru/catalog/161607624/detail.aspx"]
        }
        response = self.client.post(url, data = json.dumps(data), content_type = 'application/json')
        handle_products(response.json()['task_id'])
        url = f'/v1/offers/{response.json()["task_id"]}/'
        response = self.client.get(url)
        self.assertEqual('OK', response.json()['status'])
        self.assertEqual(200, response.status_code)

    def test_task_result_empty_list_answer(self):
        url = '/v1/offers/'
        data = {
            "regions": [213],
            "links": ["https://www.wildberries.ru/catalog/161607624/detail.aspx"]
        }
        response = self.client.post(url, data = json.dumps(data), content_type = 'application/json')
        handle_products(response.json()['task_id'])
        task_id = response.json()['task_id']
        product = Product.objects.get(offer_task = OfferTask.objects.get(id = task_id))
        product.status = 'PARSING'
        product.save()
        url = f'/v1/offers/{task_id}/'
        response = self.client.get(url)
        self.assertEqual({'count': 0, 'next': None, 'previous': None, 'results': [], 'status': 'PARSING'}, response.json())
        self.assertEqual(200, response.status_code)
