from rest_framework import serializers
from carts.models import Cart, CartItems

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = (

                'id',
                'user_id',
                'ordered',
                'amount'

        )

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = '__all__'