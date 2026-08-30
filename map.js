var map = L.map('map').setView([2.9278072, 101.6419120], 10);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

var marker = L.marker([2.9278072, 101.6419120]).addTo(map);

marker.bindPopup("MMU Cyberjaya");