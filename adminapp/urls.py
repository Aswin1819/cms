from django.urls import path
from .views import *
urlpatterns = [
    path('admin_posts/', admin_posts, name='admin_posts'),
    path('admin_comments/', admin_comments, name='admin_comments'),
    path('admin_users/', admin_users, name='admin_users'),
    path('logout/', logout_view, name='logout'),
    
]
