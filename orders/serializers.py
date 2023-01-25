from rest_framework import serializers
from stack_data import Serializer
from carts.models import Cart
from orders.models import OrderModel

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = (

                'id',
                'amount',
                'status',
                'payment_type',
                'payment_status',
                'created_at',
                'updated_at',
                'created_by',
                'cart',
                'duty'

        )
