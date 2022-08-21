from xml.dom.minidom import Document
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin', admin.site.urls),
    path('user', include('user_control.urls')),
    # API For React URLS
    path('app', include('app_control.urls')),
    # Regular Django URLS
    path('regular', include('app_control.urls_regular')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
