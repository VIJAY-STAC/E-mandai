from datetime import datetime, timedelta
from multiprocessing import context
import re
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import parsers, status, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import Group
import uuid

from yaml import serialize
from users.paginations import CustomPageNumberPagination
from seller_products.serializers import SellerProductSerializer
from seller_products.models import seller_products
from django.contrib.auth import authenticate


class BaseModelViewSet(viewsets.ModelViewSet):
    class Meta(object):
        abstract = True

class SellerProductsViewSet(BaseModelViewSet):
    model = seller_products
    serializer_class = SellerProductSerializer
    parser_classes = (parsers.FormParser, parsers.JSONParser, parsers.MultiPartParser)
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
            queryset = seller_products.objects.all().order_by('-created_at')
            return  queryset
            

    @action(detail=False, methods=["GET"])
    def seller_productlist(self, request, *args, **kwargs):
        id = request.user.id
        queryset = seller_products.objects.filter(seller_id=id)
        serializer = SellerProductSerializer(queryset,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)

