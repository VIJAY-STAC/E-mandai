from datetime import datetime, timedelta
from multiprocessing import context
import re
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import parsers, status, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import Group
import uuid
# from duties.core import sms
from yaml import serialize
from duties.utils import run_query
from orders.models import OrderModel
from users.paginations import CustomPageNumberPagination
from duties.serializers import DutySerializer
from duties.models import DutyModel
from django.contrib.auth import authenticate
from django.contrib import messages
from sms import send_sms
class BaseModelViewSet(viewsets.ModelViewSet):
    class Meta(object):
        abstract = True

class DutiesViewSet(BaseModelViewSet):
    model = DutyModel
    serializer_class = DutySerializer
    parser_classes = (parsers.FormParser, parsers.JSONParser, parsers.MultiPartParser)
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
            queryset = DutyModel.objects.all().order_by('-created_at')
            return  queryset
            


    def create(self , request, *args, **kwargs):
        user_id = request.user.id
        order_id = request.data.get('order_id')
        rider_id = request.data.get('rider_id')
        

        order = OrderModel.objects.filter(id__in = order_id)
        

        data = {
            'status':'assigned',
            'created_by':user_id,
            'rider':rider_id,
            'type':'customer'
        }
        serializer = DutySerializer(data=data)
        if serializer.is_valid(raise_exception= True):
           duty = serializer.save()
           order.update(status = 'ready_to_pickup')
           order.update(duty_id= duty.id)
          
           return Response({"message":"Duty assigned successfully " },status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False ,methods=['get'])
    def rider_assigned_duties(self, request, *args, **kwargs):
        user= request.user.id
        duty_query ='''SELECT * FROM duties_dutymodel
                        where rider_id = %s        
        ''' 

        args = (user ,)
        duty_details1 =run_query(duty_query,args)
        DutyDetails = []
        for i in range(0,len(duty_details1)):
            duty_d=duty_details1[i]
            data = {
                "duty_id":duty_d[0],
                "duty_status":duty_d[1],
                "created_at":duty_d[2],
                "type" :duty_d[6],
            }
            DutyDetails.append(data)

        return Response( {"data":DutyDetails }, status=status.HTTP_200_OK)


    @action(detail=False ,methods=['get'])
    def drop_point(self, request, *args, **kwargs):
        duty_id = request.query_params.get('duty_id')
        drop_point_query = '''SELECT  * FROM users_user 
                            where id in (SELECT distinct(created_by_id) FROM orders_ordermodel where duty_id = %s )
                    '''
        args = (duty_id, )

        print(duty_id)

        drop_point_data = run_query(drop_point_query,args)
        drop_points = []
        for i in range(0,len(drop_point_data)):
            duty = drop_point_data[i]
            data = {
                "cutomer_id":duty[0],
                "customer_name":duty[4],
                "customer_number":duty[16],
                "cutomer_address":duty[11],
                "city":duty[12],
                "pincode":duty[14]
                
            }
            drop_points.append(data)

        return Response({"data": drop_points}, status=status.HTTP_200_OK)




    @action(detail=False ,methods=['get'])
    def user_order_list_in_duty(self, request, *args, **kwargs):
        rider_id= request.user.id
        customer_id = request.query_params.get('customer_id')
        duty_id = request.query_params.get('duty_id')
        duty_query ='''SELECT oo.id ,
                            oo.status,
                            oo.payment_type,
                            oo.payment_status,
                            oo.amount,
                            sp.sp_name,
                            sp.sp_amount,
                            ci.quantity,
                            cc.amount 
                        FROM duties_dutymodel as dd
                        join orders_ordermodel as oo on oo.duty_id = dd.id
                        join carts_cart as cc on cc.id = oo.cart_id
                        join carts_cartitems as ci on cc.id = ci.cart_id
                        join seller_products_seller_products as sp on sp.id = ci.product_id
                        where  dd.rider_id = %s and oo.created_by_id = %s and oo.duty_id = %s      
        ''' 

        args = (rider_id, customer_id,duty_id ,)
        order_details =run_query(duty_query,args)
        orders = []
        for i in range(0,len(order_details)):
            duty = order_details[i]
            data = {
                "order_id":duty[0],
                "order_status":duty[1],
                "payment_type":duty[2],
                "payment_status":duty[3],
                "total_amount":duty[4],
               
                
            }
            orders.append(data)

        return Response({"data": orders}, status=status.HTTP_200_OK)

    @action(detail=False ,methods=['POST'])
    def start_duty(self, request, *args, **kwargs):
        duty_id = request.data.get('duty_id')
        duty = DutyModel.objects.get(id=duty_id)
        duty.status ='started'
        duty.save()
        order = OrderModel.objects.filter(duty_id=duty_id)
        order.update(status='picked')
        return Response({"message":"Duty started successfully"},status=status.HTTP_200_OK)

    @action(detail=False ,methods=['POST'])
    def payment_collection(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        order = OrderModel.objects.get(id=order_id)
        order.payment_status="paid"
        order.save()
        return Response({"message":"payment collected "},status=status.HTTP_200_OK)

    @action(detail=False ,methods=['POST'])
    def order_complete(self, request, *args, **kwargs):
        o_status = request.data.get('o_status')
        order_id = request.data.get('order_id')
        order = OrderModel.objects.get(id=order_id)
        if o_status =="delivered":
            o_status = "delivered"
        if o_status == "cancelled":
            o_status = "cancelled"

        order.status=o_status
        order.save()
        phone="+919130364722" 
        message = "Hi vijay message from function"
        sms(phone,message)    

        return Response({"message":"order completed succesfully ."},status=status.HTTP_200_OK)


    @action(detail=False ,methods=['POST'])
    def complete_duty(self, request, *args, **kwargs):
        duty_id = request.data.get('duty_id')
        duty = DutyModel.objects.get(id=duty_id)
        print(duty.status)
        if duty.status != 'completed':
            order_status = ['placed','ready_to_pickup','picked']
            order = OrderModel.objects.filter(duty_id=duty_id)
            for i in range(0,len(order)):
                print(order[i].status)
                if order[i].status in order_status:
                    ans = True
                else :
                    ans = False
            if ans == False :
                duty.status ='completed'
                duty.save()
                return Response({"message":"Duty completed successfully"},status=status.HTTP_200_OK)
            return Response({"message":"all orders are not delivered, please complete it on time ."},status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"Duty already completed."},status=status.HTTP_400_BAD_REQUEST)