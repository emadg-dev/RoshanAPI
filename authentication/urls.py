from django.urls import path
from .views import *

urlpatterns = [
    path('token/', login, name='token'),
    #path('token/', post_token, name='post_token'),
    path('token/logout/', logout, name='logout'),
    path('signup/', signup, name='signup'),
    
]
