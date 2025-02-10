from django.contrib import admin

# Register your models here.
from authentication.models import *

admin.site.register(Profile)
# admin.site.register(CustomUser)