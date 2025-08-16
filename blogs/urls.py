from django.urls import path
from .views import *


# app_name = 'blogs'
urlpatterns = [
    path('user_home/', user_home, name='user_home'),
    path('post_detail/<int:id>/', post_detail_view, name='post_detail'),
    path('comment-create/<int:id>/', create_comment, name='comment-create'),
    path('like/<int:id>/', like_post, name='like-post'),
    path('unlike/<int:id>/', unlike_post, name='unlike-post'),
    
]
