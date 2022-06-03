from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views import SignUpAPIView

urlpatterns = [
    path('', TokenObtainPairView.as_view(), name='obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('sign-up/', SignUpAPIView.as_view(), name='sign-up'),
]
