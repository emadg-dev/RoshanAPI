from django.urls import path
from .views import *

urlpatterns = [
    path('', ListCartItems, name='cartItems'),
    path('add/<int:pk>/', AddCartItems, name='addCartItems'),
    path('remove/<int:pk>/', RemoveCartItems, name='removeCartItems'),
    path('clear/', ClearCart, name='clearCart'),
]
