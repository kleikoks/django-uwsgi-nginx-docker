from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from core import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('project.urls'))
]

if settings.DEBUG:
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
    urlpatterns.extend(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))