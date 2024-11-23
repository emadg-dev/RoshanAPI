from django.db import models

class Category(models.Model):
    name = models.TextField(max_length=50)
    comment = models.TextField(max_length=200, default="")


class Product(models.Model):
    name = models.TextField(max_length=50)
    category = models.ForeignKey(Category, 
                                 on_delete=models.PROTECT)
    