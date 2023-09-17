from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import Token
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(write_only=True)

    class Meta:
        model  = User
        fields = ['email','first_name','last_name','password']

    def validate(self, attrs):
        email       = attrs.get('email', '')
        first_name  = attrs.get('first_name', '')
        last_name  = attrs.get('last_name', '')
        password    = attrs.get('password', '')
        if not first_name.isalpha() and not last_name.isalpha():
            raise serializers.ValidationError('the name should be have alphabet only')

        validate_password(password)

        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class LoginSerializer(serializers.ModelSerializer,TokenObtainPairSerializer):
    email       = serializers.EmailField(max_length=255,write_only=True)
    password    = serializers.CharField(write_only=True)
    tokens       = serializers.CharField(read_only=True)
    
    class Meta:
        model  = User
        fields = ['email','password','tokens']

    @classmethod
    def get_token(cls, user : User):
        Token = super().get_token(user)
        Token ['first_name'] = user.first_name
        Token ['last_name'] = user.last_name
        Token ['is_staff'] = user.is_staff
        Token ['is_superuser'] = user.is_superuser
        Token ['is_active'] = user.is_active
        return Token

    def validate(self, attrs):
        email       = attrs.get('email', '')
        password    = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)

        # import pdb
        # pdb.set_trace()

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        
        if not user.is_active:
            raise AuthenticationFailed('Your account is disabled, please contact your admin')

        return{
            # 'first_name': user.first_name,
            # 'last_name': user.last_name,
            # 'is_staff': user.is_staff,
            # 'is_superuser': user.is_superuser,
            'tokens': user.tokens()
        }
    
        return super().validate(attrs)
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user : User):
        Token = super().get_token(user)
        Token ['first_name'] = user.first_name
        Token ['last_name'] = user.last_name
        Token ['is_staff'] = user.is_staff
        Token ['is_superuser'] = user.is_superuser
        Token ['is_active'] = user.is_active
        return Token