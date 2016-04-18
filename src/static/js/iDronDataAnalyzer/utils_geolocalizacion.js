//------------------------------------------JAVASCRIPT PARA EL TEMPLATE GEOLOCALIZACIÓN----------------------------------------------

//--------------------------------CONFIGURACIÓN GOOGLE MAPS-------------------------------------------

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
  $.ajax({
	  type: 'GET',			//Obtiene la latitud y longitud inicial para posicionar el drone. Llamada AJAX al servidor.
	  url: '/updateDatosDrone',
	  data: $(this).serialize(),
	  dataType: 'json',
	  success: function (data) {
		window.lat = data[0].latitud;
		window.lng = data[0].longitud;
	  }
  });

  var myLatlng = new google.maps.LatLng(window.lat, window.lng);
  var mapOptions = {
    zoom: 15,
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
	 var cityCircle = new google.maps.Circle({
	      strokeColor: '#FF0000',
	      strokeOpacity: 0.8,
	      strokeWeight: 2,
	      fillColor: '#FF0000',
	      fillOpacity: 0.35,
	      map: map,
	      center: results[i].geometry.location,
	      radius:200
	    });
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
     title: 'Airport detected ',
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
        infowindow.setContent('Elevation at this point <br> is ' +
            results[0].elevation + ' meters.');
      } else {
        infowindow.setContent('No data');
      }
    } else {
      infowindow.setContent('Elevation service has failed because of: ' + status);
    }
  });
}

//--------------------------------ACTUALIZACIÓN DINÁMICA DE LOS DATOS RECIBIDOS DEL DRONE--------------------------------------------

function actualizarDatosDrone() {	
	  $.ajax({
		  type: 'GET',
		  url: '/updateDatosDrone',
		  data: $(this).serialize(),
		  dataType: 'json',
		  success: function (data) {
			 $('#recargar').html(
			    function(){
				var content = '<div class="col-sm-5"><label>Coordinates:&nbsp; </label><span style="font-size:80%;" class="label label-default">&nbsp;' + data[0].latitud + ', ' + data[0].longitud + '</span></div>';
				content = content + '<div class="col-sm-3"><label>Altitude:&nbsp; </label><span style="font-size:80%;" class="label label-default">&nbsp;' + data[0].altura + ' m </span></div>';
				content = content + '<div class="col-sm-3"><label>Speed:&nbsp; </label><span style="font-size:80%;" class="label label-default">&nbsp;' + data[0].velocidad + ' m/s </span></div>';
				if (data[0].alert == 1){
				   content = content + '<div style="margin-top:50px;width:90%;"><div class="alert alert-danger"><label>If you are using a drone as a hobby or recreational use:<br/><b><u>You are flying above 120 m. Be careful, it is forbidden!</u></b><br/>Remember: What I can not do with my drone? </label><ul><li>I can not fly in urban areas.</li><li>I can not fly above crowds of people: parks, beaches, wedding...</li><li>I can not fly at night.</li> <li>I can not fly close to airports, aircrafts...</li></ul></div></div>';
				}

				return content;
			    }
			)
		  }
	  });

}

setInterval(actualizarDatosDrone, 1000);

