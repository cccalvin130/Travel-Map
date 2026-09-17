

var map = L.map('map').setView([2.9278072, 101.6419120], 5);

L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors, Tiles style by Humanitarian OpenStreetMap Team'
}).addTo(map);

fetch('/api/locations/')
    .then(response => response.json())
    .then(data => {

        var places = data.locations;
        var history = document.getElementById('travel-history');
        var markers = {};
        places.forEach(function(place){

            history.innerHTML += `
                <div id="history-${place.id}"> 
                    <h3>${place.name}</h3>
                    <p>${place.city}, ${place.country}</p>
                </div>
            `;
        });    

        places.forEach(function(place) {

            document.getElementById(`history-${place.id}`).addEventListener('click', function() {

                savedLocationId = place.id;

                selectedLatitude = place.latitude;
                selectedLongitude = place.longitude;

                map.setView([place.latitude, place.longitude], 15);

                markers[place.id].openPopup();

                document.getElementById('map').scrollIntoView({
                    behavior: 'smooth'
                });

            });

        });

         places.forEach(function(place) {

            var photos="";

            if (place.photos){
                place.photos.forEach(function(photo){

                    photos += `
                        <div>
                            <img src="${photo.image}" width="150" class="photo-preview">
                            <br>
                            <button 
                                class="delete-photo-btn" 
                                data-photo-id="${photo.id}"
                                data-location-id="${place.id}">
                                Delete Photo
                            </button>
                        </div>
                    `;

                });
            }

            var popupContent = `
                <h3>${place.name}, ${place.city}, ${place.country}</h3>

                ${photos}

                <p>Latitude: ${place.latitude}</p>
                <p>Longitude: ${place.longitude}</p>

                <p>Visited: ${place.visit_date}</p>
                <p>${place.notes}</p>
            `;

            var marker = L.marker([place.latitude, place.longitude])
                .addTo(map)
                .bindPopup(popupContent);

            markers[place.id] = marker;    

            marker.on('click', function() {
                savedLocationId = place.id;

                document.getElementById('save-location-btn').textContent = 'Update Location';

                selectedLatitude = place.latitude;
                selectedLongitude = place.longitude;

                console.log('Selected Location ID:', savedLocationId);
                console.log('Selected Latitude:', selectedLatitude);
                console.log('Selected Longitude:', selectedLongitude);

                document.getElementById('location-name').value = place.name;
                document.getElementById('country').value = place.country;
                document.getElementById('city').value = place.city;
                document.getElementById('visit-date').value = place.visit_date;
                document.getElementById('notes').value = place.notes;

                alert('Location selected: ' + place.name);
            });

        });
      
    });

var currentLocationMarker = null;
var currentLatitude = null;
var currentLongitude = null;

var selectedLocationMarker = null;
var selectedLatitude = null;
var selectedLongitude = null;

var savedLocationId = null;

document.getElementById('location-btn').addEventListener('click', function() {

    if (!navigator.geolocation) {
        alert('Geolocation is not supported by this browser.');
        return;
    }

    navigator.geolocation.getCurrentPosition(
        function(position) {

            var latitude = position.coords.latitude;
            var longitude = position.coords.longitude;

            savedLocationId = null;
            document.getElementById('save-location-btn').textContent = 'Save Location';

            document.getElementById('location-name').value = '';
            document.getElementById('country').value = '';
            document.getElementById('city').value = '';
            document.getElementById('visit-date').value = '';
            document.getElementById('notes').value = '';

            currentLatitude = latitude;
            currentLongitude = longitude;

            console.log('Latitude:', latitude);
            console.log('Longitude:', longitude);

            if (currentLocationMarker) {
                map.removeLayer(currentLocationMarker);
            }

            currentLocationMarker = L.marker([latitude, longitude])
                .addTo(map)
                .bindPopup('You are here!')
                .openPopup();

            map.setView([latitude, longitude], 15);
        },

        function(error) {
            console.log(error);
            alert('Unable to get your location.');
        }
    );

});

document.getElementById('save-location-btn').addEventListener('click', function() {

    var latitude;
    var longitude;

    if (selectedLatitude !== null && selectedLongitude !== null) {
        latitude = selectedLatitude;
        longitude = selectedLongitude;
    } else if (currentLatitude !== null && currentLongitude !== null) {
        latitude = currentLatitude;
        longitude = currentLongitude;
    } else {
        alert('Please get your current location or select a location on the map.');
        return;
    } 

    var name = document.getElementById('location-name').value;
    var country = document.getElementById('country').value;
    var city = document.getElementById('city').value;
    var visitDate = document.getElementById('visit-date').value;
    var notes = document.getElementById('notes').value;

    fetch(
        savedLocationId === null
            ? '/api/locations/'
            : '/api/locations/' + savedLocationId + '/',
        {
            method: savedLocationId === null ? 'POST' : 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                country: country,
                city: city,
                latitude: latitude,
                longitude: longitude,
                visit_date: visitDate || null,
                notes: notes
            })
        }
    )
    .then(response => response.json())
    .then(data => {

        console.log(data);

        savedLocationId = data.location.id;

        console.log('Saved Location ID:', savedLocationId);

        alert('Location saved successfully!');

        location.reload();
    });

});

map.on('click', function(event) {

    var latitude = event.latlng.lat;
    var longitude = event.latlng.lng;

    savedLocationId = null;
    document.getElementById('save-location-btn').textContent = 'Save Location';

    selectedLatitude = latitude;
    selectedLongitude = longitude;

    document.getElementById('location-name').value = '';
    document.getElementById('country').value = '';
    document.getElementById('city').value = '';
    document.getElementById('visit-date').value = '';
    document.getElementById('notes').value = '';

    console.log('New location selected');
    console.log('Selected Latitude:', selectedLatitude);
    console.log('Selected Longitude:', selectedLongitude);

    if (selectedLocationMarker) {
        map.removeLayer(selectedLocationMarker);
    }

    selectedLocationMarker = L.marker([selectedLatitude, selectedLongitude])
        .addTo(map)
        .bindPopup('Selected Location')
        .openPopup();

});

document.getElementById('upload-photo-btn').addEventListener('click', function() {

    if (savedLocationId === null) {
        alert('Please select a location first.');
        return;
    }

    var photoInput = document.getElementById('photo-input');

    if (photoInput.files.length === 0) {
        alert('Please select a photo.');
        return;
    }

    var uploadRequests = [];

    for (var i = 0; i < photoInput.files.length; i++) {

        var formData = new FormData();
        formData.append('image', photoInput.files[i]);

        var uploadRequest = fetch('/api/locations/' + savedLocationId + '/photos/', {
            method: 'POST',
            body: formData
        })
        
        .then(response => response.json());

        uploadRequests.push(uploadRequest);
    }

    Promise.all(uploadRequests)
        .then(function(results) {

            console.log(results);

            alert('All photos uploaded successfully!');

            location.reload();

        })

        .catch(function(error) {

        console.log(error);

        alert('Some photos failed to upload.');
    });
});

document.getElementById('delete-location-btn').addEventListener('click', function() {

    if (savedLocationId === null) {
        alert('Please select a location first!');
        return;
    }

    var confirmed = confirm('Are you sure you want to delete this location?');

    if (!confirmed) {
        return;
    }

    fetch('/api/locations/' + savedLocationId + '/', {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {

        console.log(data);

        alert('Location deleted successfully!');

        location.reload();

    });

});

document.addEventListener('click', function(event) {

    if (event.target.classList.contains('delete-photo-btn')) {

        var photoId = event.target.dataset.photoId;
        var locationId = event.target.dataset.locationId;

        var confirmed = confirm('Are you sure you want to delete this photo?');

        if (!confirmed) {
            return;
        }

        fetch('/api/locations/' + locationId + '/photos/' + photoId + '/', {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {

            console.log(data);

            alert('Photo deleted successfully!');

            location.reload();

        });

    }

});

document.addEventListener('click', function(event) {

    if (event.target.classList.contains('photo-preview')) {

        var imageUrl = event.target.src;

        var previewWindow = window.open('', '_blank');

        previewWindow.document.write(`
            <html>
                <head>
                    <title>Photo Preview</title>
                </head>

                <body style="margin: 0; text-align: center;">
                    <img src="${imageUrl}" style="max-width: 100%; max-height: 100vh;">
                </body>
            </html>
        `);

    }

});