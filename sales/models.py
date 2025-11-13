from django.db import models
from django.contrib.auth.models import User
from products.models import Product  # 商品モデルが別アプリならimport

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)  # 農家ユーザー
