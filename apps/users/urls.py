from django.urls import path
from .views import RegisterView, CustomLoginView, MeView, LogoutView, CookieTokenRefreshView, SilentCookieTokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('me/', MeView.as_view(), name='me'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/silent/', SilentCookieTokenRefreshView.as_view(), name='silent_token_refresh')  
]
