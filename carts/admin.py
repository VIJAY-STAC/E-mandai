from django.contrib import admin

from carts.models import Cart, CartItems

# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user_id','ordered','amount']

@admin.register(CartItems)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id','cart','user','product','price','quantity']
