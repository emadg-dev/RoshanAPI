from django.db import models
from django.db import models
from django.contrib.auth.models import User
from category.models import Category
from product.models import Product

    

class ProductViewLog(models.Model):
    user = models.ForeignKey(User, 
                                on_delete=models.SET_NULL, 
                                blank=True, null=True)
    product = models.ForeignKey(Product, 
                                on_delete=models.CASCADE, 
                                blank=True)
    category =models.ForeignKey(Category, 
                                on_delete=models.CASCADE, 
                                blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} - {self.viewed_at.date()}  {self.viewed_at.strftime('%H:%M:%S')}"
    