from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=6)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username'] 

    def __str__(self):
        return self.email

class Category(models.Model):
    name = models.CharField(max_length=50)

class ContentItem(models.Model):
    title = models.CharField(max_length=30, validators=[MaxLengthValidator(30)])
    body = models.TextField(max_length=300, validators=[MaxLengthValidator(300)])
    summary = models.CharField(max_length=60, validators=[MaxLengthValidator(60)])
    document = models.FileField(upload_to='documents/', null=False, blank=False)
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
