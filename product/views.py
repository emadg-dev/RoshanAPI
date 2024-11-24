from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import ProductSerializer
from .models import *


@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def ListProduct(request):
    if request.method == 'POST':
        if not request.user.is_staff:
            return Response( {"error": "You should have appropriate privilages to do that!"},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            
            serializer.save(creator_user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

@api_view(['PUT','GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def UpdateProduct(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"error":"Product with this primary key does not exist!"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        ProductViewLog.objects.create(user=request.user, product=product)
        return Response(serializer.data)
    else:
        if not request.user.is_staff:
            return Response( {"error": "You should have appropriate privilages to do that!"},
                            status=status.HTTP_403_FORBIDDEN)
        if request.method == 'PUT':
            
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            product.delete()
            return Response({"message":"Item successfully deleted!"}, status=status.HTTP_204_NO_CONTENT)