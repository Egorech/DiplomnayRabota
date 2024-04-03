import json

from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.permissions import IsAuthenticated

from offers.paginations import ProductPagination
from offers.serializer import ProductSerializer
from users.services import BalanceService
from offers.services import RegionService, RequestDataService
from offers.models import OfferTaskRequest, OfferTask, Product

from offers.tasks import handle_products


@permission_classes((IsAuthenticated,))
@api_view(['GET', 'POST'])
def create_parsing_task(request):
    if request.method == 'GET':
        response = {
            "regions field": "list of regions for which data will be parsed",
            "links field": "list of links that will be used to parse data",
            "Example  json request on parse data:":
                {
                    "regions": [213, 2],
                    "links": [
                        "https://www.wildberries.ru/catalog/161607624/detail.aspx",
                        "https://www.wildberries.ru/catalog/143892937/detail.aspx"
                    ]
                },
            "Possible statuses:":
                {
                    "WAITING_DATA_PROCESSING": "ожидание обработки данных",
                    "DATA_PROCESSING": "обработка данных",
                    "WAITING_PARSING ": "ожидание парсинга",
                    "PARSING ": "данные в процессе парсинга",
                    "OK": "завершено",
                    "ERROR": "ошибка"
                }
        }
        return Response(response)
    try:
        data = RequestDataService.get_data_from_request(data = json.dumps(request.data, ensure_ascii = False))
        data = RegionService.get_regions_from_data(data)
    except Exception as e:
        return Response({'detail': str(e)}, status = status.HTTP_400_BAD_REQUEST)

    units = len(data['regions']) * len(data['links'])
    BalanceService.write_off_units(request.user, units)

    offer_task = OfferTask.objects.create(user = request.user)
    OfferTaskRequest.objects.create(data = data, offer_task = offer_task)

    # celery task
    handle_products.delay(offer_task.id)

    return Response({'task_id': offer_task.id,
                     'link for get answer': f"http://localhost:8000/v1/offers/{offer_task.id}/"})


class TaskResult(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        user = self.request.user
        task_id = self.kwargs['task_id']
        try:
            task = OfferTask.objects.get(id = task_id)
        except OfferTask.DoesNotExist:
            raise NotFound('No such task_id')
        if user != task.user and not user.is_superuser:
            raise PermissionDenied('This task is not yours')
        if task.task_status == 'OK':
            return Product.objects.filter(offer_task = task)
        count_parsing_status_products = Product.objects.filter(status = 'PARSING', offer_task = task).count()
        if count_parsing_status_products == 0:
            task.task_status = 'OK'
            task.save()
            return Product.objects.filter(offer_task = task)
        else:
            return []

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        task = OfferTask.objects.get(pk = kwargs['task_id'])
        response.data['status'] = task.task_status
        return response
