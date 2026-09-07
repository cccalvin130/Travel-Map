

var map = L.map('map').setView([2.9278072, 101.6419120], 5);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

fetch('/api/locations/')
    .then(response => response.json())
    .then(data => {
        var places = data.locations;
        places.forEach(function(place){

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

            L.marker([place.latitude, place.longitude])
                .addTo(map)
                .bindPopup(popupContent);

        });
      
    });

var currentLocationMarker = null;
var currentLatitude = null;
var currentLongitude = null;

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

     if (currentLatitude === null || currentLongitude === null) {
        alert('Please get your current location first.');
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
            latitude: currentLatitude,
            longitude: currentLongitude,
            visit_date: visitDate || null,
            notes: notes
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        alert('Location saved successfully!');
    });

});