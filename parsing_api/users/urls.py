from django.urls import path

from .views import *

urlpatterns = [
    path('', UserRegistrationAPIView.as_view()),
    path('accounts/profile/', get_main_info),
]