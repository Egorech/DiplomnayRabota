from offers.models import Product, OfferTask


class ProductRepository:
    @classmethod
    def create(cls, region: int, domain: str, link: str, offer_task: OfferTask, data: dict, status: str = 'PARSING') -> None:
        Product.objects.create(region=region, domain=domain, link=link, offer_task=offer_task, status=status, data = data)
