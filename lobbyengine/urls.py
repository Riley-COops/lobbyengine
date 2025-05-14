
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/authentication/', include('authentication.urls')),
    path('api/organisation/', include('organisation.urls')),
]


# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)