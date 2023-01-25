from datetime import datetime, timedelta
from multiprocessing import context
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import parsers, status, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import Group
import uuid
from users.paginations import CustomPageNumberPagination
from users.serializers import ChangePasswordSerializer, PasswordRestMailSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserSerializer
from users.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        # 'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class BaseModelViewSet(viewsets.ModelViewSet):
    class Meta(object):
        abstract = True

class UserViewSet(BaseModelViewSet):
    model = User
    serializer_class = UserSerializer
    parser_classes = (parsers.FormParser, parsers.JSONParser)
    filter_backends = (DjangoFilterBackend,)
    # permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
            queryset = User.objects.all().order_by('-created_at')
            return  queryset
            
    @action(detail=False, methods=["post"])
    def login(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')  
            user =  authenticate(email=email, password=password )
            print(user)
            if user is not None:
                u_details = User.objects.get(email=email)
                serializer = UserSerializer(u_details)
                token = get_tokens_for_user(user)
                return Response({"Data":serializer.data,"token":token},status=status.HTTP_200_OK)
            else:
                 return Response({'errors':{'non_field_errors':['Email or Password is not valid ']}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

    @action(detail=False, methods=["post"])
    def password_change(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data = request.data,context={'user': request.user})
        if serializer.is_valid():
            return Response({"message":"Password changed succesfully",},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def reset_password_link(self, request, *args, **kwargs):
        serializer = PasswordRestMailSerializer(data = request.data,)
        if serializer.is_valid(raise_exception=True):
            return Response("Password reset link sent on your registered mail id .",status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def rest_password(self, request, *args, **kwargs):
        uid = request.query_params.get('uid')   
        token = request.query_params.get('token')
        serializer = UserPasswordResetSerializer(data=request.data ,context={'uid':uid, 'token':token})
        if serializer.is_valid(raise_exception=True):
             return Response({"message":"Password reset succesfully",},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



