

var map = L.map('map').setView([2.9278072, 101.6419120], 5);

L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors, Tiles style by Humanitarian OpenStreetMap Team'
}).addTo(map);

fetch('/api/locations/')
    .then(response => response.json())
    .then(data => {

        var places = data.locations;
        var history = document.getElementById('travel-history');
        places.forEach(function(place){

            history.innerHTML += `
                <div id="history-${place.id}"> 
                    <h3>${place.name}</h3>
                    <p>${place.city}, ${place.country}</p>
                    <p>Visited: ${place.visit_date}</p>
                    <p>${place.notes}</p>
                </div>
            `;
        });    

        places.forEach(function(place) {

            document.getElementById(`history-${place.id}`).addEventListener('click', function() {

                map.setView([place.latitude, place.longitude], 15);

                document.getElementById('map').scrollIntoView({
                    behavior: 'smooth'
                });

            });

        });

         places.forEach(function(place) {

            var photos="";

            if (place.photos){
                place.photos.forEach(function(photo){
                    photos +=   `<img src="${photo.image}" width="150">`;
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

            marker.on('click', function() {
                savedLocationId = place.id;

                console.log('Selected Location ID:', savedLocationId);

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

    fetch('/api/locations/', {
        method: 'POST',
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
    })
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

    selectedLatitude = latitude;
    selectedLongitude = longitude;

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

        });
});