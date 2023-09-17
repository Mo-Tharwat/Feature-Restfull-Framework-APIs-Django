from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self,email,first_name,last_name,password=None):

        if email is None:
            raise TypeError('You must register the email')
        
        if first_name is None:
            raise TypeError('You must register your first name')
        
        if last_name is None:
            raise TypeError('You must register your last name')
        
        user = self.model(email = self.normalize_email(email),first_name=first_name ,last_name=last_name)

        validate_password(password)

        user.set_password(password)

        user.save()
        
        return user
    
    def create_superuser(self,email,first_name,last_name,password=None):

        if password is None:
            raise TypeError('You must register your password')
        
        user = self.create_user(email,first_name,last_name,password)
        user.is_superuser =True
        user.is_staff =True

        user.save()
        return user
    

class User(AbstractBaseUser,PermissionsMixin):
    email           = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name      = models.CharField(max_length=255,validators=[RegexValidator(regex='^[A-Z]{1}[a-z]{2,}$', message='Must to be first character uppercase also don\'t add any spaces', code='first_name')])
    last_name       = models.CharField(max_length=255,validators=[RegexValidator(regex='^[A-Z]{1}[a-z]{2,}$', message='Must to be first character uppercase also don\'t add any spaces', code='last_name')])
    # is_verified     = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']
    
    objects = UserManager()

    def __str__(self):
        return self.email
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }





