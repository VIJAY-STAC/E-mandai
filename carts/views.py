from datetime import datetime, timedelta
from itertools import product
from multiprocessing import context
import re
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import parsers, status, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import Group
import uuid

from yaml import serialize
from carts.utils import run_query
from users.paginations import CustomPageNumberPagination
from carts.serializers import CartItemSerializer, CartSerializer
from carts.models import CartItems,Cart
from django.contrib.auth import authenticate


class BaseModelViewSet(viewsets.ModelViewSet):
    class Meta(object):
        abstract = True

class CartViewSet(BaseModelViewSet):
    model = Cart
    serializer_class = CartSerializer
    parser_classes = (parsers.FormParser, parsers.JSONParser, parsers.MultiPartParser)
    filter_backends = (DjangoFilterBackend,)
    # permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
            queryset = Cart.objects.all()
            return  queryset
            


class BaseModelViewSet(viewsets.ModelViewSet):
    class Meta(object):
        abstract = True

class CartItemViewSet(BaseModelViewSet):
    model = CartItems
    serializer_class = CartItemSerializer
    parser_classes = (parsers.FormParser, parsers.JSONParser, parsers.MultiPartParser)
    filter_backends = (DjangoFilterBackend,)
    # permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
            queryset = CartItems.objects.all()
            return  queryset

    def create(self, request, *args, **kwargs): 
        user_id = request.user.id
        product_id = request.data.get('product')
        quantity = request.data.get('quantity')
        

        try :
            cart = Cart.objects.get(user_id_id = user_id,ordered=False)
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
                return Response({"item added successfully into the cart"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except :
            serializer = CartSerializer(data={"user_id":user_id}) 
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            cart = Cart.objects.get(user_id_id = user_id,ordered=False)
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
                return Response({"item added successfully into the cart"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            
    @action(detail=False, methods=["GET"])
    def get_cart(self, request, *args, **kwargs):
        user_id = request.user.id
        print(user_id)
        cart_details = '''SELECT * FROM carts_cartitems as ci
                            join carts_cart as cc on cc.id = ci.cart_id
                            join seller_products_seller_products as sp on sp.id = ci.product_id
                            WHERE user_id = %s AND cc.ordered= 'False'

        '''   

        args = (user_id,)     

        query_rsp = run_query(cart_details,args)
        cart_status =  query_rsp[0][7]
        if cart_status == False:
            cart_detail ={"cart_id": query_rsp[0][6],"cart_status": query_rsp[0][7],"total_amount": query_rsp[0][8]}
            cart_details = []
            for i in range(0,len(query_rsp)):
                cart_d=query_rsp[i]
                data = {
                    "cart_item_id":cart_d[0],
                    "product_img":cart_d[14],
                    "product_name":cart_d[11],
                    "mrp" :cart_d[15],
                    "quantity":cart_d[2],
                    "total_price":cart_d[1],
                }
                cart_details.append(data)
            cart_details.append(cart_detail)
            return Response(cart_details,status=status.HTTP_200_OK)
        return Response({"message":"Your cart is empty"},status=status.HTTP_200_OK)