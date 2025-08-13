# apps/users/authentication.py
import logging
from datetime import timedelta

from django.conf import settings
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from django.utils.module_loading import import_string

logger = logging.getLogger(__name__)

# Helper para leer valores de SIMPLE_JWT con defaults
def _jwt_setting(name, default=None):
    return settings.SIMPLE_JWT.get(name, default) if isinstance(settings.SIMPLE_JWT, dict) else default


class CookieJWTAuthentication(JWTAuthentication):
    """
    Authentication class that reads tokens from cookies. If access is invalid/expired
    and a refresh cookie exists and is valid, generate a new access token in-memory
    (request.new_access_token) so the response middleware can set it in cookies.
    """
    def authenticate(self, request):
        access_cookie_name = _jwt_setting("AUTH_COOKIE", "access")
        refresh_cookie_name = _jwt_setting("REFRESH_COOKIE", "refresh")
        access_token = request.COOKIES.get(access_cookie_name)
        refresh_token = request.COOKIES.get(refresh_cookie_name)

        # No tokens -> no authentication (DRF will treat as anonymous)
        if not access_token and not refresh_token:
            return None

        # Try access token first
        if access_token:
            try:
                validated = self.get_validated_token(access_token)
                user = self.get_user(validated)
                return (user, validated)
            except Exception as e:
                # access invalid/expired -> attempt refresh if available
                logger.debug("Access token invalid or expired: %s", e)

        # If we reach here, either no access token or it's invalid -> try refresh
        if not refresh_token:
            # No refresh -> authentication failed (401)
            logger.debug("No refresh token present when trying to authenticate.")
            raise exceptions.AuthenticationFailed("No hay refresh token")

        try:
            refresh = RefreshToken(refresh_token)  # validates refresh
            new_access = refresh.access_token

            # If SIMPLE_JWT provides ACCESS_TOKEN_LIFETIME, apply it (keeps consistent lifetime)
            access_lifetime = _jwt_setting("ACCESS_TOKEN_LIFETIME")
            if access_lifetime:
                try:
                    # could be timedelta
                    new_access.set_exp(lifetime=access_lifetime)
                except Exception:
                    # access_lifetime could be timedelta already; ignore on failure
                    pass

            # store token for response middleware to set cookie
            request.new_access_token = str(new_access)

            # Validate and return user
            validated = self.get_validated_token(str(new_access))
            user = self.get_user(validated)
            logger.info("Access token refreshed via refresh cookie for user id=%s", getattr(user, "id", None))
            return (user, validated)

        except TokenError as e:
            logger.info("Refresh token invalid/expired: %s", e)
            # Refresh invalid -> authentication failed -> 401
            raise exceptions.AuthenticationFailed("Sesión expirada")


    @staticmethod
    def set_auth_cookies(response, access_token=None, refresh_token=None):
        """
        Setea cookies según settings.SIMPLE_JWT (si están definidas).
        """
        access_name = _jwt_setting("AUTH_COOKIE", "access")
        refresh_name = _jwt_setting("REFRESH_COOKIE", "refresh")

        # read cookie options from SIMPLE_JWT with sensible defaults
        httponly = _jwt_setting("AUTH_COOKIE_HTTP_ONLY", True)
        secure = _jwt_setting("AUTH_COOKIE_SECURE", False)
        samesite = _jwt_setting("AUTH_COOKIE_SAMESITE", "Lax")
        path = _jwt_setting("AUTH_COOKIE_PATH", "/")
        access_max_age = None
        try:
            access_lifetime = _jwt_setting("ACCESS_TOKEN_LIFETIME")
            if access_lifetime:
                access_max_age = int(access_lifetime.total_seconds())
        except Exception:
            access_max_age = None

        if access_token:
            response.set_cookie(
                key=access_name,
                value=access_token,
                httponly=httponly,
                secure=secure,
                samesite=samesite,
                path=path,
                max_age=access_max_age,
            )

        if refresh_token:
            # for refresh cookie, use same cookie options (you can customize if needed)
            response.set_cookie(
                key=refresh_name,
                value=refresh_token,
                httponly=True,
                secure=secure,
                samesite=samesite,
                path=path,
            )

    @staticmethod
    def clear_auth_cookies(response):
        """
        Borra las cookies de auth (logout).
        """
        access_name = _jwt_setting("AUTH_COOKIE", "access")
        refresh_name = _jwt_setting("REFRESH_COOKIE", "refresh")
        response.delete_cookie(access_name, path=_jwt_setting("AUTH_COOKIE_PATH", "/"))
        response.delete_cookie(refresh_name, path=_jwt_setting("AUTH_COOKIE_PATH", "/"))


class RefreshTokenMiddleware:
    """
    Django middleware that, after the view returns, checks if the request
    has a `new_access_token` and writes it into the response cookies so the client
    receives the refreshed access token without ever seeing the 'first' 401.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        try:
            if hasattr(request, "new_access_token"):
                # Set the new access cookie (do not touch refresh unless explicitly needed)
                CookieJWTAuthentication.set_auth_cookies(
                    response,
                    access_token=request.new_access_token,
                    refresh_token=None
                )
                logger.debug("Set refreshed access cookie on response.")
        except Exception as e:
            # Never crash the whole request on cookie setting issues; log for debug
            logger.exception("Error setting refreshed access cookie: %s", e)

        return response
