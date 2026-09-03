var map = L.map('map').setView([2.9278072, 101.6419120], 5);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

var places = [
    {
        name: "Tokyo",
        country:"Japan",
        latitude: 35.6762,
        longitude: 139.6503,
        date:"20/12/2025",
        note:"My First trip to Japan!"
    },
    {
        name: "Kuala Lumpur",
        country:"Malaysia",
        latitude: 3.1390,
        longitude: 101.6869,
        date:"1/2/2026",
        note:"First time to KL"
    },
    {
        name:"MMU Cyberjaya",
        country:"Malaysia",
        latitude:2.9278072,
        longitude:101.641912,
        date:"3/9/2026",
        note:"My Foundation University!",
        images:[
            "image/business .jpg",
            "image/business 2.jpg",
            "image/business 3.jpg"
        ]

    }
];
    
places.forEach(function(place) {

    var photos = "";

    if (place.images) {

        place.images.forEach(function(image) {
            photos += `<img src="${image}" width="150">`;
        });
}

    var popupContent = `
        <h3>${place.name}, ${place.country}</h3>

        ${photos}

        <p>Visited: ${place.date}</p>
        <p>${place.note}</p>
    `;

    L.marker([place.latitude, place.longitude])
        .addTo(map)
        .bindPopup(popupContent);
});
