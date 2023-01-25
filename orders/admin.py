from django.contrib import admin
from orders.models import OrderModel
# Register your models here.
@admin.register(OrderModel)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','amount','status','payment_type','payment_status','created_at','updated_at','created_by','cart','duty']