from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

app_name = admin

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^music/', include('music.urls')),
    re_path(r'^', include('user.urls')),
    # re_path(r'^', include('music.urls')),
    re_path(r'^admin/logout/', admin.site.logout, name='logout')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
