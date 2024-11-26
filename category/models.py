from django.db import models

from django.contrib.auth.models import User

class Category(models.Model):
    name = models.TextField(max_length=50,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    creator_user = models.ForeignKey(User, 
                                 on_delete=models.PROTECT, blank=True)
    comment = models.TextField(max_length=200, default="", blank=True)
    def __str__(self):
        return f"{self.name}"
    
