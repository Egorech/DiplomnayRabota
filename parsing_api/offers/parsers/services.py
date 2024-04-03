import re


def url_get_all_offer_data(model_id: str) -> str:
    return f'https://card.wb.ru/cards/detail?appType=1&curr=rub&dest=-1257786&' \
           f'regions=80,83,38,4,64,33,68,70,30,40,86,75,69,1,66,110,22,48,31,71,112,114&' \
           f'spp=29&nm={model_id}'


def url_get_offer_analog_id(model_id: int) -> str:
    return f'https://identical-products.wildberries.ru/api/v1/identical?nmID={model_id}'


def get_model_id_from_url_with_nm(url: str) -> str:
    return re.search(r"nm=(\d+);", url).group(1)
