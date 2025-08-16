from django.shortcuts import render,redirect,get_object_or_404
from core.decorators import jwt_required
from .models import BlogPost,Comment
from authentication.models import CustomUser
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.

@jwt_required
def user_home(request):
    user = request.user
    user = get_object_or_404(CustomUser,id=user.id)
    blogs = BlogPost.objects.filter(
        is_deleted=False,
        status = 'published'
    )
    context = {
        'posts':blogs,
        'user':user
    }
    return render(request, 'user_home.html',context)


@jwt_required
def post_detail_view(request, id):
    blog = get_object_or_404(BlogPost, id=id, status='published')
    comments = Comment.objects.filter(
        post=blog,
        is_approved=True,
        ).order_by('-created_at')
    context = {
        'post':blog,
        'comments':comments
    }
    return render(request, 'post_detail.html', context)


@jwt_required
def create_comment(request, id):
    post = get_object_or_404(BlogPost, id=id, status='published')
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Comment.objects.create(
                post=post,
                user = request.user,
                content=content,
                created_at = timezone.now()
            )
            messages.success(request, "Comment Added, Waitig for the Approval")
        else:
            messages.error(request, "Comment cannot be empty")
    return redirect('post_detail', id=post.id)


@jwt_required
def like_post(request, id):
    post = get_object_or_404(BlogPost,id=id)
    post.likes.add(request.user)
    post.dislikes.remove(request.user)
    return JsonResponse({'likes_count':post.likes.count(), 'dislikes_count': post.dislikes.count()})


@jwt_required
def unlike_post(request, id):
    post = get_object_or_404(BlogPost,id=id)
    post.dislikes.add(request.user)
    post.likes.remove(request.user)
    return JsonResponse({'likes_count': post.likes.count(), 'dislikes_count': post.dislikes.count()})