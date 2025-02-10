
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/authentication', include('authentication.urls')),
    path('api/organisation', include('organisation.urls')),
    path('api/post', include('post.urls')),
    path('api/message', include('message.urls')),
    path('api/notification', include('notification.urls')),
]


# Serve media files during development
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)