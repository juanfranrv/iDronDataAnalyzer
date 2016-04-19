//------------------------------------------JAVASCRIPT PARA EL TEMPLATE GEOLOCALIZACIÓN----------------------------------------------

//--------------------------------CONFIGURACIÓN GOOGLE MAPS--------------------------------------------------------------------------

var coordenadas;
var marker;
var markers = [];
var markersCity = [];
var markersFlight = [];
var markerAirport;
var map;
var checkboxAirport = false;

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

	  if(checkboxAirport == true){
		  // Especificamos la localización, el radio y el tipo de lugar que queremos obtener para que se vaya actualizando a medida que avanza el drone
		  var service = new google.maps.places.PlacesService(map);
		  var request = {
		     location: latlng,
		     radius: 50000,
		     types: ['airport']
		   };
		 
		  service.nearbySearch(request, function(results, status) {
		     if (status === google.maps.places.PlacesServiceStatus.OK) {
		       for (var i = 0; i < results.length; i++) {
			  if(markers.length != results.length){
			     crearMarcador(results[i]);
			  }
		       }
		     }
		  });
	  }else{
		//Borra todos los marker de aeropuertos del mapa
		setMapOnAll(null);
          }
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
    zoom: 13,
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

  google.maps.event.addDomListener(window, 'load', initialize);
  setInterval(actualizarMapa, 1000);
}

function crearMarcador(place){
   // Creamos un marcador para los aeropuertos
   var markerAirport = new google.maps.Marker({
     map: map,
     position: place.geometry.location,
     title: 'Airport detected ',
     icon: '../static/images/airport.png'
   });

   markers.push(markerAirport);
}

//Borra los markers del mapa
function setMapOnAll(map) {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }

  markers = [];
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
		  url: '/updateDatosDrone',	//Vamos obteniendo los datos recogidos de la aplicación de Android y los actualizamos con AJAX sin recargar la página
		  data: $(this).serialize(),
		  dataType: 'json',
		  success: function (data) {
			 $('#recargar').html(
			    function(){
				var content = '<div class="col-sm-5"><label>Coordinates:&nbsp; </label><span style="font-size:80%;" class="label label-default">&nbsp;' + data[0].latitud + ', ' + data[0].longitud + '</span></div>';
				content = content + '<div class="col-sm-3"><label>Altitude:&nbsp; </label><span style="font-size:80%;" class="label label-default">&nbsp;' + data[0].altura + ' m </span></div>';
				content = content + '<div class="col-sm-4"><label>Speed:&nbsp; </label><span style="font-size:80%;" class="label label-default">&nbsp;' + data[0].velocidad + ' m/s </span></div>';
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

//------------------------------ACTUALIZACIÓN DINÁMICA DE DETECCIÓN DE ZONAS PROHIBIDAS--------------------------------------------------------------------

$('#airport').change(function() { 
   	if($("#airport").is(':checked')){				//Si la checkbox está seleccionada
	    checkboxAirport = true;
	} else {							//Si la checkbox no está seleccionada
	    checkboxAirport = false;
	}
});

$('#city').change(function() { 
   	if($("#city").is(':checked')){					  //Si la checkbox está seleccionada
	      activarDeteccionCiudades();
	      intervalCity = setInterval(activarDeteccionCiudades,240000);//Vamos actualizando las ciudades a medida que el drone va avanzando (cada 4 minutos)
	} else {							  //Si la checkbox no está seleccionada
	      clearInterval(intervalCity);				  //Paramos la actualización de ciudades
	      //Borra todos los marker de ciudades del mapa
	      for (var i = 0; i < markersCity.length; i++) {
	        markersCity[i].setMap(null);
	      } 

	      markersCity = [];
       }
});

$('#flight').change(function() { 
   	if($("#flight").is(':checked')){				  //Si la checkbox está seleccionada
	      activarDeteccionVuelos();
	} else {							  //Si la checkbox no está seleccionada
	      //Borra todos los marker de ciudades del mapa
	      for (var i = 0; i < markersCity.length; i++) {
	        markersFlight[i].setMap(null);
	      } 

	      markersFlight = [];
       }
});

function activarDeteccionCiudades() {					//Activa la detección de ciudades haciendo una petición a geonames en el servidor
  $.ajax({
        type: 'GET',
        url: '/getNearbyAreas',
        data: $(this).serialize(),
        dataType: 'json',
        success: function (data) {

  	   for (var i = 0; i < data.length; i++) {
		if(data.length != markersCity.length){
		   var latlng = new google.maps.LatLng(data[i].lat, data[i].lng);
		   var markerCity = new google.maps.Marker({
		     map: map,
		     position: latlng,
		     title: 'Population detected ',
		     icon: '../static/images/population.png'
		   });

   	   	   markersCity.push(markerCity);
		}
	   }
       }
   });
}

function activarDeteccionVuelos() {			//Activa la detección de vuelos haciendo una petición a flightstats en el servidor
  $.ajax({
        type: 'GET',
        url: '/getNearbyFlights',
        data: $(this).serialize(),
        dataType: 'json',
        success: function (data) {
  	   for (var i = 0; i < data.length; i++) {	//Obtenemos los vuelos y los mostramos con un marker en Google maps
		if(data.length != markersFlight.length){
		   var latlng = new google.maps.LatLng(data[i].lat, data[i].lon);
		   var markerFlight = new google.maps.Marker({
		     map: map,
		     position: latlng,
		     title: 'Plane detected: Altitude(m): ' + (Number(data[i].altitudeFt) * 0,3048) + ' - Speed(kph): ' + (Number(data[i].sppedMph) * 1,60934) + ' - date: ' + data[i].date,
		     icon: '../static/images/flight.png'
		   });

   	   	   markersFlight.push(markerFlight);
		}
	   }
       }
   });
}

