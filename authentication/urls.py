from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('token/', post_token, name='post_token'),
    path('token/logout/', logout, name='logout'),
    path('signup/', signup, name='signup'),
    
]
