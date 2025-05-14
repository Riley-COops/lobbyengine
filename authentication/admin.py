from django.contrib import admin

# Register your models here.
from authentication.models import *

admin.site.register(CustomUser)
admin.site.register(PersonalProfile)
admin.site.register(OrganisationProfile)
admin.site.register(InvestorProfile)
# admin.site.register(CustomUser)