from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from blogs.models import BlogPost, Comment
from core.decorators import superuser_required
from django.utils import timezone

User = get_user_model()

# @superuser_required
# def admin_home(request):
#     return render(request, 'admin_home.html')

@superuser_required
def admin_posts(request):
    posts = BlogPost.objects.all()
    total_posts = posts.count()
    featured_posts = posts.filter(status='published', featured=True).count() if hasattr(BlogPost, 'featured') else 0
    context = {
        'posts': posts,
        'total_posts': total_posts,
        'featured_posts': featured_posts,
    }
    return render(request, 'admin_posts.html', context)

@superuser_required
def admin_comments(request):
    comments = Comment.objects.all()
    total_comments = comments.count()
    approved_comments = comments.filter(is_approved=True).count()
    pending_comments = comments.filter(is_approved=False).count()
    context = {
        'comments': comments,
        'total_comments': total_comments,
        'approved_comments': approved_comments,
        'pending_comments': pending_comments,
    }
    return render(request, 'admin_comments.html', context)

@superuser_required
def admin_users(request):
    users = User.objects.all()
    total_users = users.count()
    active_users = users.filter(is_active=True).count()
    admin_users = users.filter(is_staff=True).count()
    recent_signups = users.filter(date_joined__gte=timezone.now()-timezone.timedelta(days=7)).count()
    context = {
        'users': users,
        'total_users': total_users,
        'active_users': active_users,
        'admin_users': admin_users,
        'recent_signups': recent_signups,
    }
    return render(request, 'admin_user.html', context)


@superuser_required
def logout_view(request):
    response = redirect("login")
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response
    
    
