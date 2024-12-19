# urls.py
from django.urls import path, include
from rest_framework import routers
from .views import UserRegistrationView, ProfileView

router = routers.DefaultRouter()
router.register(r'users', UserRegistrationView, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', ProfileView.as_view(), name='profile'),  # Direct profile access for the logged-in user
    path('auth/', include('djoser.urls')),  # Djoser endpoints for user and password management
    path('auth/', include('djoser.urls.authtoken')),  # Token-based login/logout
]
