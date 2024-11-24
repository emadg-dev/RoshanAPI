from django.db import models
from django.contrib.auth.models import User
from category.models import Category


class Product(models.Model):
    name = models.TextField(max_length=50 ,unique=True)
    category = models.ForeignKey(Category, 
                                 on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    creator_user = models.ForeignKey(User, 
                                 on_delete=models.PROTECT, blank=True)
    price = models.FloatField(default=0, blank=True)

class ProductViewLog(models.Model):
    user = models.ForeignKey(User, 
                                on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, 
                                on_delete=models.CASCADE, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)