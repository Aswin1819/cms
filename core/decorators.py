from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse
from functools import wraps


def _login_redirect(request):
    """Redirect to login with next parameter pointing back to current path."""
    login_url = reverse('login')
    next_param = request.get_full_path()
    return redirect(f"{login_url}?next={next_param}")


def jwt_required(view_func):
    """
    Allow access only to authenticated users. If not authenticated, redirect to login.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return _login_redirect(request)
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def superuser_required(view_func):
    """
    Allows access only to authenticated superusers. Redirects unauthenticated users to login.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return _login_redirect(request)
        if not request.user.is_superuser:
            return HttpResponseForbidden("You do not have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view