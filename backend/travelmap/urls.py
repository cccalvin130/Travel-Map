"""
URL configuration for travelmap project.

Main routing file - all URLs are dispatched from here.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from locations.views import main_map, profile_page, login_page, register_page, logout_page

urlpatterns=[
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout/', logout_page, name='logout'),
    path('', main_map, name='main-map'),
    path('profile/', profile_page, name='profile-page'),

    # Django admin interface
    path('admin/', admin.site.urls),

    # Our API endpoints
    # All URLs starting with /api/ are handled by the locations app's urls.py
    # For example, /api/locations/ matches 'locations/' in locations/urls.py
    path('api/', include('locations.urls')),
]

# Configure media file (user-uploaded images) access path
# This only works in development mode (DEBUG=True).
# In production, use a web server like Nginx to serve static files.
# Meaning: when accessing /media/xxx.jpg, Django looks for the file in MEDIA_ROOT
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
