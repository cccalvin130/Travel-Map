

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
                <h3>${place.name}, ${place.country}</h3>

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

document.getElementById('location-btn').addEventListener('click', function() {

    if (!navigator.geolocation) {
        alert('Geolocation is not supported by this browser.');
        return;
    }

    navigator.geolocation.getCurrentPosition(
        function(position) {

            var latitude = position.coords.latitude;
            var longitude = position.coords.longitude;

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

            fetch('/api/locations/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: 'Current Location',
                    country: '',
                    city: '',
                    latitude: latitude,
                    longitude: longitude,
                    visit_date: null,
                    notes: 'Saved from current location'
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
            });
        },

        function(error) {
            console.log(error);
            alert('Unable to get your location.');
        }
    );

});