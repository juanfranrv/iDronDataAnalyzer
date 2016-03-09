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
	          coordenadas = data;	//Cogemos coordenadas del drone del servidor y vamos actualizando la posición en el mapa
	          var latlng = new google.maps.LatLng(coordenadas[0], coordenadas[1]);
	          marker.setPosition(latlng);
	          map.setCenter(latlng); 

		   // Especificamos la localización, el radio y el tipo de lugares que queremos obtener para que se vaya actualizando a medida que avanza el drone
		  var service = new google.maps.places.PlacesService(map);
		  var request = {
		     location: latlng,
		     radius: 50000,
		     types: ['airport']
		   };
		 
		   service.nearbySearch(request, function(results, status) {
		     if (status === google.maps.places.PlacesServiceStatus.OK) {
		       for (var i = 0; i < results.length; i++) {
			 crearMarcador(results[i]);
		       }
		     }
		   });
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
  // Creamos el servicio PlaceService y enviamos la petición.
  var service = new google.maps.places.PlacesService(map);
 

  // Lanza la elevación del terreno al dar click a una zona
  map.addListener('click', function(event) {
     displayLocationElevation(event.latLng, elevator, infowindow);
  });

   // Especificamos la localización, el radio y el tipo de lugares que queremos obtener
   var request = {
     location: myLatlng,
     radius: 50000,
     types: ['airport']
   };
 
   service.nearbySearch(request, function(results, status) {
     if (status === google.maps.places.PlacesServiceStatus.OK) {
       for (var i = 0; i < results.length; i++) {
         crearMarcador(results[i]);
       }
     }
   });

  google.maps.event.addDomListener(window, 'load', initialize);
  setInterval(actualizarMapa, 1000);
}

function crearMarcador(place){
   // Creamos un marcador para los aeropuertos
   var marker = new google.maps.Marker({
     map: map,
     position: place.geometry.location,
     title: 'Aeropuerto detectado',
     icon: '../static/images/airport.png'
   });
}

function displayLocationElevation(location, elevator, infowindow) {
  // Petición de localización
  elevator.getElevationForLocations({
    'locations': [location]
  }, function(results, status) {
    infowindow.setPosition(location);
    if (status === google.maps.ElevationStatus.OK) {
      // Cogemos el primer resultado
      if (results[0]) {
        // Abrimos la infowindow para mostrar la elevación en el punto deseado
        infowindow.setContent('La elevación en este punto <br>es ' +
            results[0].elevation + ' metros.');
      } else {
        infowindow.setContent('No se han obtenido resultados');
      }
    } else {
      infowindow.setContent('El servicio de elevación ha fallado debido a: ' + status);
    }
  });
}

