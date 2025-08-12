# core/middleware.py
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser

class JWTAuthMiddleware(MiddlewareMixin):
    """
    Middleware that authenticates requests using JWT tokens
    stored in HttpOnly cookies (or in Authorization header as fallback).
    Sets request.user for normal Django views.
    """

    def process_request(self, request):
        # Default to anonymous
        request.user = AnonymousUser()
        auth = JWTAuthentication()

        raw_token = None

        #First, try to get token from HttpOnly cookie
        cookie_token = request.COOKIES.get("access_token")
        if cookie_token:
            raw_token = cookie_token

        # If not in cookie, fallback to Authorization header
        if raw_token is None:
            header = auth.get_header(request)
            if header is not None:
                raw_token = auth.get_raw_token(header)

        #  If still no token, leave as AnonymousUser
        if raw_token is None:
            return

        #  Validate token and set request.user
        try:
            validated_token = auth.get_validated_token(raw_token)
            request.user = auth.get_user(validated_token)
        except Exception:
            request.user = AnonymousUser()
