from django.db import models


class Location(models.Model):
    """
    Location table - stores places the user has visited
    Django will automatically create a database table,
    each location is one row in the table.
    """

    # Name of the place, e.g. "Eiffel Tower"
    # CharField = text field, max_length = maximum number of characters
    name = models.CharField(max_length=200)

    # Country, e.g. "France"
    country = models.CharField(max_length=100)

    # City, e.g. "Paris"
    city = models.CharField(max_length=100)

    # Latitude, e.g. 48.8584
    # FloatField = decimal number (floating point)
    latitude = models.FloatField()

    # Longitude, e.g. 2.2945
    longitude = models.FloatField()

    # Date of visit, e.g. 2024-06-15
    # DateField = date (year-month-day)
    # blank=True, null=True = optional field (user may not remember the date)
    visit_date = models.DateField(blank=True, null=True)

    # Personal notes, thoughts or memories about the place
    # TextField = long text with no character limit
    notes = models.TextField(blank=True)

    # Creation timestamp, automatically set
    # auto_now_add = automatically set to current time when created, never changes
    created_at = models.DateTimeField(auto_now_add=True)

    # Last updated timestamp, automatically updated
    # auto_now = automatically updated to current time on every save
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # What to display when printing this location object
        # e.g. "Eiffel Tower (France, Paris)"
        return self.name + " (" + self.country + ", " + self.city + ")"


class Photo(models.Model):
    """
    Photo table - stores photos for each location
    One location can have multiple photos, so we use a ForeignKey
    to link photos to the Location table.
    """

    # Which location this photo belongs to
    # ForeignKey = links to the Location table (many-to-one relationship)
    # on_delete=models.CASCADE = if location is deleted, delete its photos too
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    # Image file
    # ImageField = designed for images, automatically validates that upload is an image
    # upload_to = folder where images are stored
    image = models.ImageField(upload_to='location_photos/')

    # Photo description, e.g. "Eiffel Tower at sunset", optional
    description = models.CharField(max_length=200, blank=True)

    # Upload timestamp, automatically set
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # What to display when printing this photo object
        # e.g. "Eiffel Tower - Photo"
        return self.location.name + " - Photo"
