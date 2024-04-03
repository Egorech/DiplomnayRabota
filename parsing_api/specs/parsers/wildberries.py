import json
import requests

from specs.models import Product


def url_spec(spec: str) -> str:
    return f'https://search.wb.ru/exactmatch/ru/common/v4/search?TestGroup=control&TestID=188&appType=1&curr=rub&' \
           f'dest=-1257786&query={spec}&regions=80,38,4,64,83,33,68,70,69,30,86,75,40,1,66,110,22,31,48,71,114&' \
           f'resultset=catalog&sort=popular&spp=0&suppressSpellcheck=false'


def dataparser(product_id: int, serialized_data: str):
    wildberries_data = requests.get(url_spec(serialized_data)).text

    # данные после запроса
    wildberries_data = json.loads(wildberries_data)['data']['products']

    dict_list = []

    for wildberries_item in wildberries_data:
        try:
            dict_specs = {'id': wildberries_item['id'],
                          'name': wildberries_item['name'],
                          'link': f"https://www.wildberries.ru/catalog/{wildberries_item['id']}/detail.aspx",
                          'brand': wildberries_item['brand'],
                          'rating': wildberries_item['rating'],
                          'feedbacks': wildberries_item['feedbacks']}
            dict_list.append(dict_specs)
        except Exception:
            continue

    product = Product.objects.get(id = product_id)
    product.data['answer'] = dict_list

    product.status = 'OK'
    product.save()

    return None
