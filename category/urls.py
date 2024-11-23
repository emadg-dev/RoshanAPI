from django.urls import path
from .views import *

urlpatterns = [
    path('',ListCategory , name='listCategory'),
]
