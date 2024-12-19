from django.urls import path, include
from rest_framework import routers
from .views import OrganisationViewSet

router = routers.DefaultRouter()
router.register(r'organisations', OrganisationViewSet, basename='organisations')

urlpatterns = [
    path('', include(router.urls)),
]