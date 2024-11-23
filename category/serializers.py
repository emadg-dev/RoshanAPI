from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'comment', 'created_at', 'creator_user']