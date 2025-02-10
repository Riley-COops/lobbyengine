# urls.py
from django.urls import path, include
from rest_framework import routers
from authentication.views import AuthenticationView, ProfileView

# router = routers.DefaultRouter()
# router.register(r'auth', AuthenticationView, basename='authentication')

urlpatterns = [
    # path('', include(router.urls)),
    path("auth/", AuthenticationView.as_view(), name="authentication"),
    path('profile/', ProfileView.as_view(), name='profile'),  # Direct profile access for the logged-in user
    path('auth/', include('djoser.urls')),  # Djoser endpoints for user and password management
    path('auth/', include('djoser.urls.authtoken')),  # Token-based login/logout
]
