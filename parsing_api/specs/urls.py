from django.urls import path

from . import views

urlpatterns = [
    path('', views.create_parsing_task),
    path('<int:task_id>/', views.TaskResult.as_view())
]