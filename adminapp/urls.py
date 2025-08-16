from django.urls import path
from .views import *
urlpatterns = [
    path('admin_posts/', admin_posts, name='admin_posts'),
    path('admin_create_post/', admin_create_post, name='admin_create_post'),
    path('admin_edit_post/<int:id>/', admin_edit_post, name='admin_edit_post'),
    path('admin_delete_post/<int:id>/', admin_delete_post, name='admin_delete_post'),
    path('admin_comments/', admin_comments, name='admin_comments'),
    path('admin_approve_comment/<int:id>/', admin_approve_comment, name='admin_approve_comment'),
    path('admin_users/', admin_users, name='admin_users'),
    path('admin_edit_user/<int:id>/',admin_edit_users, name='admin_edit_user'),
    path('admin_delete_user/<int:id>/', admin_delete_users, name='admin_delete_user'),
    path('logout/', logout_view, name='logout'),
]
