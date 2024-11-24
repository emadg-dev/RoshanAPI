from django.urls import path
from .views import *

urlpatterns = [
    path('',ListCategory , name='listCategory'),
    path('<int:pk>/', UpdateCategory , name='updateCategory'),
    path('<int:pk>/products/', ListCategoryProducts , name='listCategoryProducts'),
]
