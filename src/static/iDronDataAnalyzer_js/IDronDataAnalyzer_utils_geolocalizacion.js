//------------------------------------------JAVASCRIPT PARA EL TEMPLATE GEOLOCALIZACIÓN----------------------------------------------


var coordenadas;
var marker;
var map;

function actualizarMapa() {
  $.ajax({
	        type: 'GET',
	        url: '/coordenadas',
	        data: $(this).serialize(),
	        dataType: 'json',
	        success: function (data) {
	          coordenadas = data;
	          var latlng = new google.maps.LatLng(coordenadas[0], coordenadas[1]);
	          marker.setPosition(latlng);
	          map.setCenter(latlng); 
	        }
   });
}

function initialize() {
  var myLatlng = new google.maps.LatLng(37.19699469878369, -3.6241040674591507);
  var mapOptions = {
    zoom: 12,
    center: myLatlng,
    mapTypeId: 'terrain'
  }
  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
  marker = new google.maps.Marker({
      position: myLatlng,
      map: map,
      title: 'Drone',
      icon: '../static/images/dron_geo.png'
  });

  var elevator = new google.maps.ElevationService;
  var infowindow = new google.maps.InfoWindow({map: map});

  // Add a listener for the click event. Display the elevation for the LatLng of
  // the click inside the infowindow.
  map.addListener('click', function(event) {
    displayLocationElevation(event.latLng, elevator, infowindow);
  });

  google.maps.event.addDomListener(window, 'load', initialize);
  setInterval(actualizarMapa, 1000);
}

function displayLocationElevation(location, elevator, infowindow) {
  // Initiate the location request
  elevator.getElevationForLocations({
    'locations': [location]
  }, function(results, status) {
    infowindow.setPosition(location);
    if (status === google.maps.ElevationStatus.OK) {
      // Retrieve the first result
      if (results[0]) {
        // Open the infowindow indicating the elevation at the clicked position.
        infowindow.setContent('La elevación en este punto <br>es ' +
            results[0].elevation + ' metros.');
      } else {
        infowindow.setContent('No se han obtenido resultados');
      }
    } else {
      infowindow.setContent('El servicio de elevación ha fallaod debido a: ' + status);
    }
  });
}

