from django.contrib import admin
from seller_products.models import seller_products

# Register your models here.
@admin.register(seller_products)
class SellerProductAdmin(admin.ModelAdmin):
    list_display = ['id','sp_name','sp_description','sp_validity','sp_img','sp_amount','sp_stock','seller_id','created_at','updated_at']
