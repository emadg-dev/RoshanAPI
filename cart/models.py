from django.db import models
from django.contrib.auth.models import User

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    creator_user = models.ForeignKey(User, 
                                 on_delete=models.PROTECT, blank=True)
    comment = models.TextField(max_length=200, default="", blank=True)
    user = models.ForeignKey(User,
                              on_delete=models.PROTECT, blank=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, 
                                 on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    creator_user = models.ForeignKey(User, 
                                 on_delete=models.PROTECT, blank=True)
    