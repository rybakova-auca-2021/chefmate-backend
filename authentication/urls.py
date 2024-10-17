from django.urls import path
from authentication.views import (
    RegisterView,
    RegisterWithEmailView,
    LoginView,
    TokenRefreshView,
    LogoutView,
    SendCodeView,
    UserProfileUpdateView,
    UserMeView,
    PasswordResetView,
    PasswordSetView
)


urlpatterns = [
    path('login/', LoginView.as_view(), name='user-login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='user-registration'),
    path('register-with-email/', RegisterWithEmailView.as_view(), name='user-registration-with-email'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('set-new-password/', PasswordSetView.as_view(), name='set-new-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('send-code/<int:user_id>/', SendCodeView.as_view(), name='send-code'),
    path('profile/update/<int:user_id>/', UserProfileUpdateView.as_view(), name='profile-update'),
    path('me/<int:user_id>/', UserMeView.as_view(), name='users-me'),
]
