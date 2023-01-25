from click import style
from django.conf import settings
from pyrsistent import field
from rest_framework import serializers
from django.utils.encoding import force_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from users.utils import *
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password',}, write_only=True)
    class Meta:
        model = User
        fields = (
            
           'id',
           'email',
           'name',
           'date_of_birth',
           'phone_number',
           'user_type',
           'address',
           'pincode',
           'city',
           'country',
           'tc', 
           'is_admin',
           'password',
           'password2'
        )
        extra_kwargs = {'password':{'write_only':True}}

    def validate(self,value):
        password =value.get('password')
        password2 = value.get('password2')
        if password != password2 :
            raise serializers.ValidationError("Password and confirm password doesn't match")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']
        

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100)
    password2 = serializers.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self, value):
        password =value.get('password')
        password2 = value.get('password2')
        user = self.context.get('user')
        if password != password2 :
            raise serializers.ValidationError("Password and confirm password doesn't match")
        user.set_password(password)
        user.save()
        return value

class PasswordRestMailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email']

    def validate(self, value):
        email = value.get('email')  
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'https://localhost:3000/api/user/reset/'+uid+'/'+token
            #send email
            data={
                    'subject' :"Password Reset Link From E-Mandai ",
                    'body' : "To Reset the Password click here : " + link,
                    'to_email' : user.email

            } 
            send_email(data)        
            return value
        else:
            raise serializers.ValidationError("You are not registered user")

class UserPasswordResetSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100)
    password2 = serializers.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self, value):
       try:
            password =value.get('password')
            password2 = value.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2 :
                raise serializers.ValidationError("Password and confirm password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):    
                raise serializers.ValidationError("Token is invalid or expired")
            user.set_password(password)
            user.save()
            return value
       except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token) 
            raise serializers.ValidationError("Token is invalid or expired")