from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import *
from .models import *
from product.models import Product
from product.serializers import ProductSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ListCartItems(request):
    user = request.user
    cart = CartItem.objects.filter(user = user)
    if not cart.exists():
        return Response({"message": "You don't have any items in your cart!"},
                         status=status.HTTP_204_NO_CONTENT)

    serializer = CartItemSerializer(cart, many=True)
    return Response(serializer.data)

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def AddCartItems(request, pk):
    user = request.user
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"error":"Product with this primary key does not exist!"}, 
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'POST':
        try:
            cartItem = CartItem.objects.get(user=user, product=product)
            cartItem.quantity += 1
        except CartItem.DoesNotExist:
            cartItem = CartItem(product=product, user=user)

        cartItem.save()
        cart = CartItem.objects.filter(user = user)
        serializer = CartItemSerializer(cart, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET','DELETE'])
@permission_classes([IsAuthenticated])
def RemoveCartItems(request, pk):
    user = request.user
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"error":"Product with this primary key does not exist!"}, 
                        status=status.HTTP_404_NOT_FOUND)
    try:
        cartItem = CartItem.objects.get(user=user, product=product)    
    except CartItem.DoesNotExist:
        return Response({"error":"This product is not in your cart!"}, 
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CartItemSerializer(cartItem)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        cartItem.delete()
        cart = CartItem.objects.filter(user = user)
        serializer = CartItemSerializer(cart, many=True)
        return Response({"message":f"item {product.name}, has been removed from your cart!"},
                                status=status.HTTP_202_ACCEPTED)
    
    

@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def ClearCart(request):
    user = request.user
    cart = CartItem.objects.filter(user = user)
    if not cart.exists():
        return Response({"message": "You don't have any items in your cart!"},
                        status=status.HTTP_204_NO_CONTENT)
    else:
        if request.method == 'GET':
            serializer = CartItemSerializer(cart, many=True)
            return Response(serializer.data)
        
        elif request.method == 'DELETE':
            cart.delete()
            return Response({"message":"Your cart has been successfully cleared!"},
                            status=status.HTTP_204_NO_CONTENT)