from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializer import UserSerializer


class UserRegistrationAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response({'info': f'You are already authenticated, create new user or go to this url to get main info: '
                                     f'http://localhost:8000/accounts/profile/'})
        else:
            required_fields = ['username', 'email', 'first_name', 'last_name', 'password']
            return Response({'info': f'All registration fields are required: {required_fields}'})

    def post(self, request):
        required_fields = ['username', 'email', 'first_name', 'last_name', 'password']
        data = request.data

        # Проверяем наличие всех обязательных полей регистрации
        if not all(field in data for field in required_fields):
            return Response({'error': f'All registration fields are required: {required_fields}'},
                            status = status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data = data)
        if serializer.is_valid():
            user = serializer.save()

            response_data = {
                'username': user.username,
                'password': data.get('password'),
                'units': user.units,
                'url for authentication': 'http://localhost:8000/v1/drf-auth/login/'
            }
            return Response(response_data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_main_info(request):
    user = request.user

    response_data = {
        'username': user.username,
        'email': user.email,
        'units': user.units,
        'parse offers': 'http://localhost:8000/v1/offers/',
        'parse specs': 'http://localhost:8000/v1/specs/'
    }
    return Response(response_data)
