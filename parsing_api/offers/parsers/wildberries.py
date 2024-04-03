import json

from offers.models import Product, Offer
from offers.parsers.services import *
import requests


def dataparser(product_id: int, serialized_data: int):
    wildberries_data = requests.get(url_get_offer_analog_id(serialized_data)).text  # [1, 2, 3] -> str

    # удаление скобок из строки
    wildberries_data = wildberries_data.strip('[]')

    # разделение строки по запятым и преобразование каждого элемента в целое число
    wildberries_data = [int(item) for item in wildberries_data.split(',')] if len(wildberries_data) > 0 else []

    # формирование строки для нового запроса
    wildberries_data.insert(0, serialized_data)
    wildberries_data = [str(elem) for elem in wildberries_data]
    wildberries_data = ';'.join(wildberries_data) if len(wildberries_data) > 1 else wildberries_data[0] + ';'
    url = url_get_all_offer_data(wildberries_data)
    wildberries_data = requests.get(url).text

    # данные после запроса
    wildberries_data = json.loads(wildberries_data)['data']['products']

    dict_list = []

    for wildberries_item in wildberries_data:
        try:
            dict_offers = {'id': get_model_id_from_url_with_nm(url),
                           'name': wildberries_item['name'],
                           'price': wildberries_item['priceU'] // 100,
                           'sale_price': wildberries_item['salePriceU'] // 100}
            dict_list.append(dict_offers)
        except Exception:
            continue

    product = Product.objects.get(id = product_id)
    Offer.objects.create(product = product, data = dict_list)

    product.status = 'OK'
    product.save()

    return None
