from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from crm import views

# Defining the URL patterns for the project.
urlpatterns = [
    # URL pattern for the admin site.
    path("admin/", admin.site.urls),
    # Including the URL patterns from the 'crm' application.
    path("", include("crm.urls")),
]

# Serving static files during development.
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serving media files during development.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
