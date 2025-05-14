# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, AddMemberView, RemoveMemberView

router = DefaultRouter()
router.register(r'teams', TeamViewSet, basename='team')

urlpatterns = [
    path('', include(router.urls)),
    path('teams/<int:team_id>/add-member/', AddMemberView.as_view(), name='add-member'),
    path('teams/<int:team_id>/remove-member/<int:user_id>/', RemoveMemberView.as_view(), name='remove-member'),
]
