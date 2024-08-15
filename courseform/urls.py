from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings



admin.site.site_header = "Courseform  Superadmin"
admin.site.site_title = "Courseform Superadmin Portal"
admin.site.index_title = "Welcome to Courseform  Superadmin Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('formsystem.urls')),
  
]


# Retrieve images from /media/
urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
