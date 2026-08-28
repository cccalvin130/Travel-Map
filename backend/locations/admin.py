from django.contrib import admin
from .models import Location, Photo

# Register the Location model with the admin interface
# After registration, you can view and manage location data at http://127.0.0.1:8000/admin/
admin.site.register(Location)

# Register the Photo model with the admin interface
# After registration, you can view and manage photo data in the admin panel
admin.site.register(Photo)
