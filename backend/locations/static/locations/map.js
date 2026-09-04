

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
