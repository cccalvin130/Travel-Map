from django.urls import path
from . import views

"""
URL routing configuration - maps URLs to view functions

Naming conventions:
- List endpoints use plural nouns, e.g. /api/locations/
- Detail endpoints use /api/locations/<id>/
- Sub-resources use nested paths, e.g. /api/locations/<id>/photos/
"""

urlpatterns = [
    # Location list: get all locations / create a new location
    path('locations/', views.location_list, name='location-list'),

    # Location detail: get / update / delete a single location
    # <int:location_id> extracts an integer from the URL and passes it as location_id to the view
    path('locations/<int:location_id>/', views.location_detail, name='location-detail'),

    # Photo list for a location: get all photos / upload a new photo
    path('locations/<int:location_id>/photos/', views.photo_list, name='photo-list'),

    # Single photo: delete a photo
    path('locations/<int:location_id>/photos/<int:photo_id>/', views.photo_detail, name='photo-detail'),
]
