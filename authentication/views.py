from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):

    username=request.data['username']
    password=request.data['password']
    if not username or not password: 
        return Response({"error": "Please insert valid values for username and password!"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username=username)
        if not user.check_password(password):
            return Response({"error": "Invalid username or password!"}, status=status.HTTP_404_NOT_FOUND)
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        response = Response({"token": token.key, "user":serializer.data})
        response.set_cookie(
            key='auth_token',
            value=token.key,
            httponly=True, 
            secure=False,
            samesite='lax'
        )
        return response 
    except User.DoesNotExist:
        return Response({"error": "Invalid username or password!"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        response = Response({"token": token.key, "user": serializer.data})
        response.set_cookie(
            key='auth_token',
            value=token.key,
            httponly=True, 
            secure=False,
            samesite='lax'
        )
        return response
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['POST']) 
@permission_classes([IsAuthenticated])
def logout(request):
    if request.user.is_authenticated:
        try:
            token = Token.objects.get(user=request.user)
            #token.delete()
        except Token.DoesNotExist:
            return Response({"error": "token not found!"}, status=status.HTTP_404_NOT_FOUND)
        response = Response({"message": "User logged out successfully!"}, status=status.HTTP_200_OK)
        response.delete_cookie('auth_token')
        return response
    return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED) 


@api_view(['POST'])
@permission_classes([AllowAny])
def post_token(request):
    token_key = request.data['token']
    if not token_key:
        return Response({"error": "Please insert a valid value for token!"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        token = Token.objects.get(key=token_key)
        user = token.user
        serializer = UserSerializer(user)
        response = Response({"user": serializer.data})
        response.set_cookie(
            key='auth_token',
            value=token.key,
            httponly=True, 
            secure=False,
            samesite='lax'
        )
        return response
    
    except Token.DoesNotExist:
        return Response({"error":"Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home(request):
    return Response({"message": f"Hello, {request.user.username}!"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home(request):
    return Response({"message": f"Hello, {request.user.username}!"})
