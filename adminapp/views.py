from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from blogs.models import BlogPost, Comment
from core.decorators import superuser_required
from django.utils import timezone
from .forms import PostForm
from django.contrib import messages

User = get_user_model()

# @superuser_required
# def admin_home(request):
#     return render(request, 'admin_home.html')

@superuser_required
def admin_posts(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    total_posts = posts.count()
    featured_posts = posts.filter(status='published', featured=True).count() if hasattr(BlogPost, 'featured') else 0
    context = {
        'posts': posts,
        'total_posts': total_posts,
        'featured_posts': featured_posts,
    }
    return render(request, 'admin_posts.html', context)


@superuser_required
def admin_create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                messages.success(request, 'Blog post created successfully!')
                return redirect('admin_posts')  # or wherever you want to redirect
            except Exception as e:
                messages.error(request, f'Error creating post: {str(e)}')
                print(f'Error creating post: {str(e)}')
        else:
            # Print form errors for debugging
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
                    print(f'{field}: {error}')
    else:
        form = PostForm()
    
    return render(request, 'admin_create_post.html', {'form': form})




@superuser_required
def admin_edit_post(request, id):
    post = get_object_or_404(BlogPost,id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            print("form edited successfully")
            return redirect('admin_posts')
        else:
            print("Form Edit fail:",form.errors)
    else:
        form = PostForm(instance=post)
    return render(request, 'admin_edit_post.html', {'form':form, 'post':post})

    


@superuser_required
def admin_delete_post(request, id):
    post = get_object_or_404(BlogPost, id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('admin_posts')
    context = {'post': post}
    return render(request, 'admin_delete_post.html', context)

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
    users = User.objects.filter(is_deleted=False)
    total_users = users.count()
    active_users = users.filter(is_active=True).count()
    admin_users = users.filter(is_superuser=True).count()
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
def admin_edit_users(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        username = request.POST.get('username', user.username)
        email = request.POST.get('email', user.email)
        is_active = request.POST.get('is_active') == 'on'
        is_staff = request.POST.get('is_staff') == 'on'
        bio = request.POST.get('bio', user.bio)
        user.username = username
        user.email = email
        user.is_active = is_active
        user.is_staff = is_staff
        user.bio = bio
        user.save()
        return redirect('admin_users')
    return redirect('admin_users')


@superuser_required
def admin_delete_users(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user.delete()
        return redirect('admin_users')
    return redirect('admin_users')

@superuser_required
def logout_view(request):
    response = redirect("login")
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response
    
    
