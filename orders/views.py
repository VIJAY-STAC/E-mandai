from datetime import datetime, timedelta
from multiprocessing import context
import re
from django.http import QueryDict
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import parsers, status, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import Group
import uuid

from yaml import serialize
# from duties.core import sms
from users.models import User
from carts.serializers import CartItemSerializer, CartSerializer
from carts.models import Cart
from orders.paginations import CustomPageNumberPagination
from orders.serializers import OrdersSerializer
from orders.models import OrderModel
from django.contrib.auth import authenticate




class BaseModelViewSet(viewsets.ModelViewSet):
    class Meta(object):
        abstract = True

class OrdersViewSet(BaseModelViewSet):
    model = OrderModel
    serializer_class = OrdersSerializer
    parser_classes = (parsers.FormParser, parsers.JSONParser, parsers.MultiPartParser)
    filter_backends = (DjangoFilterBackend,)
    # permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
            queryset = OrderModel.objects.all()
            return  queryset
            
    def create(self, request, *args, **kwargs):
        cart_id = request.data.get('cart')
        print(cart_id)
        cart = Cart.objects.get(id=cart_id)
        if cart.ordered == False:
            serializer = OrdersSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                cart.ordered = True
                cart.save()
                return Response({"message": "order created dsuccesfully"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST )
        return Response({"message": "Order is already created"}, status=status.HTTP_400_BAD_REQUEST )

    @action(detail=False, methods=["POST"])
    def place_single_order(self , request, *args, **kwargs):
        user_id = request.user.id
        product_id = request.data.get('product')
        quantity = request.data.get('quantity')
        payment_type = request.data.get('payment_type')
        status = request.data.get('status')
        payment_status = request.data.get('payment_status')
        u_name = request.user.name
        u_no =str(request.user.phone_number)
        print(u_no)

        message = "Dear "+u_name+",your order has been placed . Thank you for shopping on E-Mandia. Keep shopping, stay healthy "

        serializer = CartSerializer(data={"user_id":user_id}) 
        if serializer.is_valid(raise_exception=True):
            cart = serializer.save()
        cart_id = cart.id
        cart_item_data={
                "cart": cart_id,
                "user": user_id,
                "product" : product_id,
                "quantity" : quantity
        }

        serializer = CartItemSerializer(data= cart_item_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        cart_details = Cart.objects.get(id=cart_id)

        order_data= {
            	"amount": cart_details.amount,
                "status":"placed",
                "payment_type": payment_type,
                "payment_status":payment_status,
                "created_by":user_id,
                "cart": cart_id        
        }


        serializer = OrdersSerializer(data=order_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            cart_details.ordered = True
            cart_details.save()
            
            return Response({"message": "order created dsuccesfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST )
        
    @action(detail=False, methods=["POST"])
    def Query(self, request, *args, **kwargs):
        Queryset = OrderModel.objects.aggregate(amount= sum('id'))
        print(Queryset)

        
