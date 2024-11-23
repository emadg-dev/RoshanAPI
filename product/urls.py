from django.urls import path
from .views import *

urlpatterns = [
    path('', ListProduct, name='listProduct'),
    path('<int:pk>/', UpdateProduct, name='updateProduct'),
]
