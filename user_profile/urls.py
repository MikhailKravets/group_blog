from django.urls import path

from user_profile.views import ProfileViewSet

urlpatterns = [
    path('password/change/', ProfileViewSet.as_view({'put': 'change_password'}), name='password'),
    path('', ProfileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update'}), name='profile'),
]
