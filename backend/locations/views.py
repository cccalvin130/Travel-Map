import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Location, Photo

def main_map(request):
    return render(request,'locations/Main_Map.html')

def location_to_dict(location):
    """
    Convert a Location object to a dictionary.
    Django objects cannot be sent directly to the frontend,
    so we convert them to dictionaries first, then to JSON.
    """
    # Create an empty dictionary
    result = {}

    # Add each field to the dictionary
    result['id'] = location.id
    result['name'] = location.name
    result['country'] = location.country
    result['city'] = location.city
    result['latitude'] = location.latitude
    result['longitude'] = location.longitude

    # Visit date may be empty, so we need to check
    if location.visit_date:
        result['visit_date'] = str(location.visit_date)
    else:
        result['visit_date'] = None

    result['notes'] = location.notes

    # Add all photos for this location
    # Note: since we removed related_name in models.py, we use photo_set
    photos = []
    for photo in location.photo_set.all():
        photo_dict = {
            'id': photo.id,
            'image': photo.image.url,
            'description': photo.description,
        }
        photos.append(photo_dict)
    result['photos'] = photos

    return result


@csrf_exempt
def location_list(request):
    """
    Location list API endpoint
    URL: /api/locations/
    GET = get all locations
    POST = create a new location
    """

    if request.method == 'GET':
        # Get all locations from the database
        all_locations = Location.objects.all()

        # Convert each location to a dictionary and add to a list
        result = []
        for location in all_locations:
            location_dict = location_to_dict(location)
            result.append(location_dict)

        # Return the result to the frontend
        return JsonResponse({'locations': result})

    elif request.method == 'POST':
        # Read data sent by the frontend and convert to dictionary
        data = json.loads(request.body)

        # Extract each field from the dictionary
        name = data['name']
        country = data['country']
        city = data['city']
        latitude = data['latitude']
        longitude = data['longitude']

        # These two fields are optional, use .get() with default values
        visit_date = data.get('visit_date')
        notes = data.get('notes', '')

        # Create a new location and save to database
        new_location = Location.objects.create(
            name=name,
            country=country,
            city=city,
            latitude=latitude,
            longitude=longitude,
            visit_date=visit_date,
            notes=notes,
        )

        # Return success message and the new location data
        return JsonResponse({
            'message': 'Created successfully',
            'location': location_to_dict(new_location),
        })


@csrf_exempt
def location_detail(request, location_id):
    """
    Single location API endpoint
    URL: /api/locations/<location_id>/
    GET = get details of one location
    PUT = update one location
    DELETE = delete one location
    """

    # Find location by id, returns None if not found
    location = Location.objects.filter(id=location_id).first()

    # Return error if location not found
    if not location:
        return JsonResponse({'error': 'Location not found'}, status=404)

    if request.method == 'GET':
        # Return this location's data
        return JsonResponse({'location': location_to_dict(location)})

    elif request.method == 'PUT':
        # Read data sent by the frontend
        data = json.loads(request.body)

        # Update field only if frontend provided it, otherwise keep original value
        if 'name' in data:
            location.name = data['name']
        if 'country' in data:
            location.country = data['country']
        if 'city' in data:
            location.city = data['city']
        if 'latitude' in data:
            location.latitude = data['latitude']
        if 'longitude' in data:
            location.longitude = data['longitude']
        if 'visit_date' in data:
            location.visit_date = data['visit_date']
        if 'notes' in data:
            location.notes = data['notes']

        # Save changes to database
        location.save()

        return JsonResponse({
            'message': 'Updated successfully',
            'location': location_to_dict(location),
        })

    elif request.method == 'DELETE':
        # Delete this location
        # Note: when location is deleted, all its photos are also deleted
        # automatically (because of CASCADE on the ForeignKey)
        location.delete()
        return JsonResponse({'message': 'Deleted successfully'})


@csrf_exempt
def photo_list(request, location_id):
    """
    Photo list API endpoint
    URL: /api/locations/<location_id>/photos/
    GET = get all photos for a location
    POST = upload a new photo to a location
    """

    # First find the location
    location = Location.objects.filter(id=location_id).first()
    if not location:
        return JsonResponse({'error': 'Location not found'}, status=404)

    if request.method == 'GET':
        # Get all photos for this location
        all_photos = location.photo_set.all()

        # Convert to list of dictionaries
        result = []
        for photo in all_photos:
            photo_dict = {
                'id': photo.id,
                'image': photo.image.url,
                'description': photo.description,
            }
            result.append(photo_dict)

        return JsonResponse({'photos': result})

    elif request.method == 'POST':
        # Get the uploaded image from the request
        # Note: image upload cannot use JSON, must use form data (multipart/form-data)
        image_file = request.FILES['image']

        # Get photo description, optional
        description = request.POST.get('description', '')

        # Create a new photo and save to database
        new_photo = Photo.objects.create(
            location=location,
            image=image_file,
            description=description,
        )

        return JsonResponse({
            'message': 'Photo uploaded successfully',
            'photo': {
                'id': new_photo.id,
                'image': new_photo.image.url,
                'description': new_photo.description,
            },
        })


@csrf_exempt
def photo_detail(request, location_id, photo_id):
    """
    Single photo API endpoint
    URL: /api/locations/<location_id>/photos/<photo_id>/
    DELETE = delete one photo
    """

    # First find the location
    location = Location.objects.filter(id=location_id).first()
    if not location:
        return JsonResponse({'error': 'Location not found'}, status=404)

    # Then find the photo that belongs to this location
    photo = location.photo_set.filter(id=photo_id).first()
    if not photo:
        return JsonResponse({'error': 'Photo not found'}, status=404)

    if request.method == 'DELETE':
        # Delete the photo
        photo.delete()
        return JsonResponse({'message': 'Photo deleted successfully'})
