from rest_framework import serializers
from .models import *
from product.serializers import ProductSerializer

# class CartSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Cart
#         fields = ['id', 'created_at', 'creator_user', 'comment', 'user']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True) 
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'created_at', 'user', 'comment']