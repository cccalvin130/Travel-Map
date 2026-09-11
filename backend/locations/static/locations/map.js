// Get the map container
const mapContainer = document.getElementById("map");

// Create ECharts map
const map = echarts.init(mapContainer);


// Load world map data
fetch("/static/locations/world.json")
    .then(response => response.json())
    .then(worldJson => {

        // Register the world map
        echarts.registerMap("world", worldJson);


        // Get saved locations from Django Backend
        return fetch("/api/locations/")
            .then(response => response.json())
            .then(data => {

                const places = data.locations;

                // Convert backend locations into ECharts data
                const locationData = places.map(place => {

                    return {
                        name: place.name,

                        value: [
                            Number(place.longitude),
                            Number(place.latitude)
                        ],

                        location: place
                    };

                });


                // Display the map
                map.setOption({

                    title: {
                        text: "My Travel Map",
                        left: "center"
                    },


                    tooltip: {
                        trigger: "item",

                        formatter: function (params) {

                            // Country hover
                            if (!params.data || !params.data.location) {
                                return params.name;
                            }

                            // Location marker
                            const place = params.data.location;

                            return `
                                <b>${place.name}</b><br>
                                ${place.city}, ${place.country}<br>
                                Latitude: ${place.latitude}<br>
                                Longitude: ${place.longitude}
                            `;
                        }
                    },


                    geo: {
                        map: "world",
                        roam: true,

                        itemStyle: {
                            areaColor: "#e6e6e6",
                            borderColor: "#888"
                        },

                        emphasis: {
                            itemStyle: {
                                areaColor: "#cfcfcf"
                            }
                        }
                    },


                    // Travel location markers
                    series: [

                        {
                            name: "Travel Locations",

                            type: "scatter",

                            coordinateSystem: "geo",

                            data: locationData,

                            symbol: "pin",

                            symbolSize: 35
                        }

                    ]

                });

            });

    })
    .catch(error => {

        console.error("Failed to load map or locations:", error);

    });


// Make the map responsive
window.addEventListener("resize", function () {
    map.resize();
});

// Select a location by clicking on the map
map.on("click", function (params) {

    // Get the clicked position
    const pointInPixel = [params.event.offsetX, params.event.offsetY];

    const pointInGeo = map.convertFromPixel(
        { geoIndex: 0 },
        pointInPixel
    );

    const longitude = pointInGeo[0];
    const latitude = pointInGeo[1];

    console.log("Selected Latitude:", latitude);
    console.log("Selected Longitude:", longitude);

});