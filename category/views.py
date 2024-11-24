from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import CategorySerializer
from .models import Category
from product.models import Product
from product.serializers import ProductSerializer

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def ListCategory(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        if not request.user.is_staff:
            return Response( {"error": "You should have appropriate privilages to do that!"},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = CategorySerializer(data = request.data)
        if serializer.is_valid():
            
            serializer.save(creator_user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT','GET', 'DELETE'])
@permission_classes([IsAdminUser])
def UpdateCategory(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({"error":"Category with this primary key does not exist!"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        category.delete()
        return Response({"message":"Item successfully deleted!"}, status=status.HTTP_204_NO_CONTENT)
    
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def ListCategoryProducts(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({"error":"Category with this primary key does not exist!"},
                         status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        products = Product.objects.filter(category=category.pk)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        product_id = request.data.get('pk')
        if product_id:
            try:
                product = Product.objects.get(pk=product_id)
                product.category = category
                product.save()
                products = Product.objects.filter(category=category.pk)
                serializer = ProductSerializer(products, many=True)
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            except Product.DoesNotExist:
                return Response({"error":"Product with this primary key does not exist!"},
                         status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)