from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RegisterSerializer, LoginSerializer, CustomTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.

class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        user =request.data
        serializer=self.serializer_class(data=user)

        if serializer.is_valid():
            #serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message':'User registered successfully'}, status=status.HTTP_201_CREATED)

        # user_data = serializer.data

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        return Response(str(CustomTokenObtainPairView()), status=status.HTTP_200_OK)
    
        # if serializer.is_valid():
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        
        # return Response(serializer.errors, status.HTTP_401_UNAUTHORIZED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    token_obtain_pair = TokenObtainPairView.as_view()