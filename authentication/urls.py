from django.urls import path
from .views import RegisterView, LoginAPIView, CustomTokenObtainPairView

urlpatterns = [
    path('register/',RegisterView.as_view(), name='register'),
    path('login/',LoginAPIView.as_view(), name='login'),
]