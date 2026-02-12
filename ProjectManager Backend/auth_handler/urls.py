from django.urls import path
from auth_handler.views import RegisterAPIView, LoginAPIView, TokenRefreshAPIView, TokenVerifyAPIView, MeAPIView

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="auth-register"),
    path("login/", LoginAPIView.as_view(), name="auth-login"),
    path("token/refresh/", TokenRefreshAPIView.as_view(), name="auth-token-refresh"),
    path("token/verify/", TokenVerifyAPIView.as_view(), name="auth-token-verify"),
    path("me/", MeAPIView.as_view(), name="auth-me"),
]
