import json

from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.permissions import IsAuthenticated

from specs.paginations import ProductPagination
from specs.serializer import ProductSerializer
from specs.models import SpecTask, SpecTaskRequest, Product
from users.services import BalanceService
from specs.services import RequestDataService
from specs.tasks import handle_products


@permission_classes((IsAuthenticated,))
@api_view(['GET', 'POST'])
def create_parsing_task(request):
    if request.method == 'GET':
        response = {
            "site_products field": "list of names of items whose characteristics you want to know",
            "links field": "domain string",
            "Example  json request on parse data:":
                {
                    "site_products": ['jbl 310', 'jbl'],
                    "domain": "wildberries.ru"
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
    except Exception as e:
        return Response({'detail': str(e)}, status = status.HTTP_400_BAD_REQUEST)

    units = len(data['site_products'])
    BalanceService.write_off_units(request.user, units)

    spec_task = SpecTask.objects.create(user = request.user)
    SpecTaskRequest.objects.create(data = data, spec_task = spec_task)

    # celery task
    handle_products.delay(spec_task.id)

    return Response({'task_id': spec_task.id,
                    'link for get answer': f"http://localhost:8000/v1/specs/{spec_task.id}/"})


class TaskResult(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        user = self.request.user
        task_id = self.kwargs['task_id']
        try:
            task = SpecTask.objects.get(id = task_id)
        except SpecTask.DoesNotExist:
            raise NotFound('No such task_id')
        if self.request.user != task.user and not user.is_superuser:
            raise PermissionDenied('This task is not yours')
        if task.task_status == 'OK':
            return Product.objects.filter(spec_task = task)
        count_parsing_status_products = Product.objects.filter(status = 'PARSING', spec_task = task).count()
        if count_parsing_status_products == 0:
            task.task_status = 'OK'
            task.save()
            return Product.objects.filter(spec_task = task)
        else:
            return []

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        task = SpecTask.objects.get(pk = kwargs['task_id'])
        response.data['status'] = task.task_status
        return response
