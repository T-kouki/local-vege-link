from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

class Product(models.Model):
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='products'
    )
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)  

    def __str__(self):
        return self.name


# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('farm', 'Farm'),
        ('eat', 'Eat'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    familyname = models.CharField(max_length=50, blank=True) # 姓
    lastname = models.CharField(max_length=50, blank=True)  # 名
    nickname = models.CharField(max_length=30, blank=True)  # 表示される名前
    email = models.EmailField(unique=True)                     # メールアドレス
    address = models.CharField(max_length=255, blank=True)  # 住所
    phone_number = models.CharField(max_length=20, blank=True)  # 電話番号
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)  # 販売実績が確認できる書類
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='eat')

    def __str__(self):
        return self.nickname
class Inquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"


class Item(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default=1)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, default=1)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.IntegerField()  # price × quantity
    date = models.DateTimeField(auto_now_add=True)
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - {self.total_price}円"

class FarmerRating(models.Model):
    farmer = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='ratings_given'
    )
    score = models.IntegerField()  # 星1〜5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.farmer.nickname} - {self.score}"
