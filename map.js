// Create the map
const map = L.map("map").setView([4.2105, 101.9758], 6);

// Add OpenStreetMap
L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

L.marker([3.1390, 101.6869])
    .addTo(map)
    .bindPopup("<b>Kuala Lumpur</b><br>Capital of Malaysia.");