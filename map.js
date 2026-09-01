var map = L.map('map').setView([2.9278072, 101.6419120], 5);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

var places = [
    {
        name: "Tokyo",
        latitude: 35.6762,
        longitude: 139.6503
    },
    {
        name: "Kuala Lumpur",
        latitude: 3.1390,
        longitude: 101.6869
    },
    {
        name: "Singapore",
        latitude: 1.3521,
        longitude: 103.8198
    },
    {
        name: "Bangkok",
        latitude: 13.7563,
        longitude: 100.5018
    },
    {
        name:"MMU Cyberjaya",
        latitude:2.9278072,
        longitude:101.641912
    }
];
    
places.forEach(function(place) {
    L.marker([place.latitude, place.longitude])
        .addTo(map)
        .bindPopup(place.name);
});
