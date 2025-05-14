from django.urls import path
from .views import CustomRegistrationView, InvestorProfileView, PersonalProfileView, OrganisationProfileView, AddOrganisationToInvestorView, UnifiedProfileView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView


urlpatterns = [
    path('register/', CustomRegistrationView.as_view(), name='register'),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/jwt/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    #Profile views
    path('profile/', UnifiedProfileView.as_view(), name='unified_profile'),
    path('personal/', PersonalProfileView.as_view(), name='personal_profile'),
    path('organisation/', OrganisationProfileView.as_view(), name='organisation_profile'),
    path('investor/', InvestorProfileView.as_view(), name='investor_profile'),
    path('investor/add-organisation/', AddOrganisationToInvestorView.as_view(), name='add_organisation_to_investor'),
    
    
]