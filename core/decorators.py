from django.http import HttpResponseForbidden
from functools import wraps


def jwt_required(view_func):
    """
    Allow access only to authenticated users
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden('Authentication Required')
        return view_func(request, *args, **kwargs)
    return _wrapped_view



def superuser_required(view_func):
    """
    Allows access only to authenticated superusers.
    Uses request.user set by JWTAuthMiddleware.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Authentication required.")
        if not request.user.is_superuser:
            return HttpResponseForbidden("You do not have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view