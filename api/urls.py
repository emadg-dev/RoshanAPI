from django.urls import path
from .views import *

urlpatterns = [
    path('auth/login/', login, name='login'),
    path('auth/token/', post_token, name='post_token'),
    path('auth/token/logout/', logout, name='logout'),
    path('auth/signup/', signup, name='signup'),
    path('home/', home, name='home'),
]
