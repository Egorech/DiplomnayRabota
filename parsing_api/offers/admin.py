from django.contrib import admin
from offers.models import OfferTaskRequest, OfferTask, Product, Offer


# Регистрируем модель OfferTaskRequest
@admin.register(OfferTaskRequest)
class OfferTaskRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'offer_task', 'data')
    list_filter = ('offer_task',)
    search_fields = ('id', 'offer_task__id')

# Регистрируем модель OfferTask
@admin.register(OfferTask)
class OfferTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_status', 'user')
    list_filter = ('task_status', 'user')
    search_fields = ('id', 'task_status', 'user__username')

# Регистрируем модель Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'offer_task', 'region', 'domain', 'link', 'status', 'data')
    list_filter = ('offer_task', 'status')
    search_fields = ('id', 'offer_task__id', 'domain', 'link')

# Регистрируем модель Offer
@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'data')
    list_filter = ('product',)
    search_fields = ('id', 'product__id')
