from django.contrib import admin
from .models import SpecTaskRequest, SpecTask, Product


@admin.register(SpecTaskRequest)
class SpecTaskRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'spec_task')
    list_filter = ('spec_task',)
    search_fields = ('id', 'spec_task__task_status')


@admin.register(SpecTask)
class SpecTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_status', 'user')
    list_filter = ('task_status',)
    search_fields = ('id', 'user__username')
    raw_id_fields = ('user',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'spec_task', 'domain', 'data')
    list_filter = ('spec_task__task_status',)
    search_fields = ('id', 'spec_task__id', 'domain')
