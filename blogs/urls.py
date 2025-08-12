from django.urls import path
from .views import *


# app_name = 'blogs'
urlpatterns = [
    path('user_home/', user_home, name='user_home'),
]
