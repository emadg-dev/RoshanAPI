from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import CategorySerializer
from .models import Category

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def ListCategory(request):
    if request.method == 'POST':
        if not request.user.is_staff:
            return Response( {"error": "You should have appropriate privilages to do that!"},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = CategorySerializer(data = request.data)
        if serializer.is_valid():
            
            serializer.save(creator_user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)