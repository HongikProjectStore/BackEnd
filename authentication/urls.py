from django.urls import path
from .views import LogoutView, ProfileView, RegisterView, VerifyEmail, ChangePasswordView
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views


router = routers.SimpleRouter()

urlpatterns = router.urls + [
    path('register/', RegisterView.as_view(), name="register"),
    #path('login/', LoginAPIView.as_view(), name="login_legacy"),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('email_verify/', VerifyEmail.as_view(), name="email_verify"),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
