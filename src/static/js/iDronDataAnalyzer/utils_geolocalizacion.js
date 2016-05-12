//------------------------------------------JAVASCRIPT PARA EL TEMPLATE GEOLOCALIZACIÓN----------------------------------------------

//--------------------------------CONFIGURACIÓN GOOGLE MAPS--------------------------------------------------------------------------

var coordenadas;
var marker;
var map;
var markers = [], markersFlight = [], markersCity = [];				//Array para almacenar cada uno de los marker de las zonas detectadas
var markersCityCircle = [], markersFlightCircle = [], markersCircle = [];	//Array para almacenar las áreas de círculos que simbolizan las zonas prohibidas
var totalResults = 0, totalResultsCity = 0, totalResultsFlight = 0;		//Variable contador para llevar el número de marker que borraremos al seleccionarlo
var checkboxAirport = false, checkboxCity = false, checkboxFlight = false;	//Variables que indican si cada checkbox ha sido pulsado
var airportDetected = false, flightDetected = false, cityDetected = false;	//Variables que indican si se ha entrado en zona prohibida
var num_CityDetected = 100, num_airportDetected = 100, num_flightDetected = 100 ;  //Variables que almacenan la última zona restringida invadida (iniciadas a 100)

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
		 
		  service.nearbySearch(request, function(results, status) {	//Actualizamos aeropuertos a medida que el drone va avanzando
		     if (status === google.maps.places.PlacesServiceStatus.OK) {
		       for (var i = 0; i < results.length; i++) {
			  if((markers.length + markersCircle.length) != (results.length + totalResults)){
			     crearMarcador(results[i]);
			     var cityCircle = new google.maps.Circle({		//Dibujamos un círculo y un marker en cada aeropuerto
			 	      strokeColor: '#FF0000',
			 	      strokeOpacity: 0.8,
			 	      strokeWeight: 2,
			 	      fillColor: '#FF0000',
			 	      fillOpacity: 0.35,
			 	      map: map,
			 	      center: results[i].geometry.location,
			 	      radius:800
			      });

			      markersCircle.push(cityCircle);	 //Almacenamos los círculos en un array para borrarlos cuando se desee
			      totalResults += 1                  //Incrementamos el contador cada vez que añadimos un círculo para borrarlo posteriormente
			  }
		       }
		     }
		  });
	  }else{
		//Borra todos los marker de aeropuertos del mapa
		  for (var i = 0; i < markers.length; i++) {
		    markers[i].setMap(null);
		    markersCircle[i].setMap(null);
		  }

		  totalResults = 0;
		  markers = [];					//Reset de los array 
		  markersCircle = [];
          }

	  if(checkboxCity == true){	//Si el checkbox de ciudad está activo, comprobamos si el drone está contenido en el área para informar al usuario
	       for (var i = 0; i < markersCityCircle.length; i++) {
		   if(markersCityCircle[i].getBounds().contains(latlng)){
			cityDetected = true;
			num_CityDetected = i;	//Almacenado la última ciudad invadida
		   }

		   if(num_CityDetected != 100){	//Nunca habrá 100 ciudades en la misma zona
			   //Si la última ciudad contenida, ya no se encuentra contenida, quitamos alerta
			   if(markersCityCircle[num_CityDetected].getBounds().contains(latlng) == false){ 
				cityDetected = false;
				num_CityDetected = 100;
			   }
		   }
		}

	  }else{

	     cityDetected = false;
	  }

	  if(checkboxAirport == true){  //Si el checkbox de aeropuerto está activo, comprobamos si el drone está contenido en el área para informar al usuario
	       for (var i = 0; i < markersCircle.length; i++) {
		   if(markersCircle[i].getBounds().contains(latlng)){
			airportDetected = true;
			num_airportDetected = i;	//Almacenamos el último aeropuerto invadido
		   }

		   if(num_airportDetected != 100){	//Nunca habrá 100 aeropuertos en la misma zona
			   //Si el último aeropuerto contenido, ya no se encuentra contenido, quitamos alerta
			   if(markersCircle[num_airportDetected].getBounds().contains(latlng) == false){ 
				airportDetected = false;
				num_airportDetected = 100;
			   }
		   }
	       }

	  }else{

	     airportDetected = false;
	  }

	  if(checkboxFlight == true){ //Si el checkbox de detección de aviones está activo, comprobamos si el drone está contenido en el área para informar al usuario
	       for (var i = 0; i < markersFlightCircle.length; i++) {
		   if(markersFlightCircle[i].getBounds().contains(latlng)){
			flightDetected = true;
			num_flightDetected = i;		//Almacenado el último vuelo invadido
		   }

		   if(num_flightDetected != 100){	//Nunca habrá 100 vuelos en la misma zona
			   //Si el último vuelo contenido ya no se encuentra contenido, quitamos alerta
			   if(markersFlightCircle[num_flightDetected].getBounds().contains(latlng) == false){ 
				flightDetected = false;
				num_flightDetected = 100;
			   }
		   }
	       }

	  }else{

	     flightDetected = false;
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
	marker = new google.maps.Marker({			//Creamos el marker del drone
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
				var content = '<div style="float:left;"><label>Coordinates:&nbsp; </label><span style="font-size:80%;" class="label label-default">&nbsp;' + data[0].latitud + ', ' + data[0].longitud + '</span></div>';
				content = content + '<div style="float:left; margin-left:10%"><label>Altitude:&nbsp; </label><span style="font-size:80%;" class="label label-default">&nbsp;' + data[0].altura + ' m</span></div>';
				content = content + '<div style="float:left; margin-left:10%;"><label>Speed:&nbsp; </label><span style="font-size:80%;" class="label label-default">&nbsp;' + data[0].velocidad + ' m/s</span></div>';
				
				if (data[0].alert == 1){	//Si se supera los 120m de altitud, informamos al usuario
				   content = content + '<div style="margin-top:50px;"><div class="alert alert-danger"><label>If you are using a drone as a hobby or recreational use:<br/><b><u>You are flying above 120 m. Be careful, it is forbidden!</u></b><br/>Remember: What can not I do with my drone? </label><ul><li>I can not fly in urban areas.</li><li>I can not fly above crowds of people: parks, beaches, wedding...</li><li>I can not fly at night.</li> <li>I can not fly close to airports, aircrafts...</li></ul></div></div>';
				}

				if (flightDetected == true){   //Si se entra en zona prohibida (vuelo detectado), informamos al usuario
				   content = content + '<div style="margin-top:50px;"><div class="alert alert-danger"><label><u>Warning:</u> You are inside a forbidden area. You are flying near a plane.</label></div>';
				}

				if (airportDetected == true){   //Si se entra en zona prohibida (aeropuerto detectado), informamos al usuario
				   content = content + '<div style="margin-top:50px;"><div class="alert alert-danger"><label><u>Warning:</u> You are inside a forbidden area. You are flying near an airport.</label></div>';
				}

				if (cityDetected == true){      //Si se entra en zona prohibida (ciudad detectada), informamos al usuario
				   content = content + '<div style="margin-top:50px;"><div class="alert alert-danger"><label><u>Warning:</u> You are inside a forbidden area. You are flying near a populated place.</label></div>';
				}
				
				//Activa sonido cuando hay una alerta
				if(data[0].alert ==1 || flightDetected == true || airportDetected == true || cityDetected == true){
				   content = content + '<audio style="visibility:hidden" controls autoplay><source src="../static/sound/alerta.mp3" type="audio/mpeg"></audio>';
				}

				return content;
			    }
			)
		  }
	  });
}

setInterval(actualizarDatosDrone, 1000);		//Actualizamos la información cada segundo periódicamente

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
              checkboxCity = true;
	      activarDeteccionCiudades();
	      intervalCity = setInterval(activarDeteccionCiudades,120000);//Vamos actualizando las ciudades a medida que el drone va avanzando (cada 2 minutos)

	} else {							  //Si la checkbox no está seleccionada
	      checkboxCity = false;
	      clearInterval(intervalCity);				  //Paramos la actualización de ciudades
	      //Borra todos los marker de ciudades del mapa
	      for (var i = 0; i < markersCity.length; i++) {
	        markersCity[i].setMap(null);
		markersCityCircle[i].setMap(null);
	      } 

	      markersCity = [];
	      markersCityCircle = [];
	      totalResultsCity = 0;
       }
});

$('#flight').change(function() { 
   	if($("#flight").is(':checked')){				  //Si la checkbox está seleccionada
	      activarDeteccionVuelos();
              checkboxFlight = true;
	} else {							  //Si la checkbox no está seleccionada
              checkboxFlight = false;
	      //Borra todos los marker de vuelos del mapa
	      for (var i = 0; i < markersFlight.length; i++) {
	        markersFlight[i].setMap(null);
		markersFlightCircle[i].setMap(null);
	      } 
	      //Reset de los arrays
	      markersFlight = [];
	      markersFlightCircle = [];
	      totalResultsFlight = 0;
       }
});

function activarDeteccionCiudades() {					       //Activa la detección de ciudades haciendo una petición a geonames en el servidor
  $.ajax({
        type: 'GET',
        url: '/getNearbyAreas',
        data: $(this).serialize(),
        dataType: 'json',
        success: function (data) {

           if(data == 'Geonames web service is temporarily unavailable.'){     //Si el servicio web da error, informamos al usuario, en caso contrario mostramos datos

	       $('#fail').html(
		      function(){
			 var content = '<div style="margin-top:50px;"><div class="alert alert-danger"><label><u>Error: </u>' + data + '</label></div>';
			  return content;
		      }
	       )

	   }else{

	  	   for (var i = 0; i < data.length; i++) {

			//Comprobamos si el marker existe para no volver a crearlo
			if((markersCity.length + markersCityCircle.length) != (data.length + totalResultsCity)){

			   var latlng = new google.maps.LatLng(data[i].lat, data[i].lng);
			   var markerCity = new google.maps.Marker({			//Creamos el marker y el círculo correspondiente
			     map: map,
			     position: latlng,
			     title: 'Population detected: ' + data[i].toponymName,
			     icon: '../static/images/population.png'
			   });
			   var PopulationCircle = new google.maps.Circle({
			 	      strokeColor: '#2E9AFE',
			 	      strokeOpacity: 0.8,
			 	      strokeWeight: 2,
			 	      fillColor: '#2E9AFE',
			 	      fillOpacity: 0.35,
			 	      map: map,
			 	      center: latlng,
			 	      radius:4800
			   });

	   	   	   markersCity.push(markerCity);				//Lo añadimos a cada array para borrarlo cuando el usuario lo seleccione
	   	   	   markersCityCircle.push(PopulationCircle);
			   totalResultsCity += 1;
			}
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

          if(data == 'Flightstats web service is temporarily unavailable.'){	//Si el servicio web da error, informamos al usuario, en caso contrario mostramos datos

	       $('#fail').html(
		      function(){
			 var content = '<div style="margin-top:50px;"><div class="alert alert-danger"><label><u>Error: </u>' + data + '</label></div>';
			  return content;
		      }
	       )

	   }else{

	  	   for (var i = 0; i < data.length; i++) {	//Obtenemos los vuelos y los mostramos con un marker en Google maps
			if((markersFlight.length + markersFlightCircle.length) != (data.length + totalResultsFlight)){

			   var latlng = new google.maps.LatLng(data[i].lat, data[i].lon);
			   var markerFlight = new google.maps.Marker({	//Creamos un marker con la información del vuelo
			     map: map,
			     position: latlng,
			     title: 'Plane detected: Altitude(m): ' + Math.round((Number(data[i].altitudeFt) * 0.3048)) + ' - Speed(kph): ' + Math.round((Number(data[i].speedMph) * 1.60934)) + ' - date: ' + data[i].date,
			     icon: '../static/images/flight.png'
			   });

			   var flightCircle = new google.maps.Circle({
			 	      strokeColor: '#64FE2E',
			 	      strokeOpacity: 0.8,
			 	      strokeWeight: 2,
			 	      fillColor: '#64FE2E',
			 	      fillOpacity: 0.35,
			 	      map: map,
			 	      center: latlng,
			 	      radius:800
			   });

	   	   	   markersFlight.push(markerFlight);		//Almacenamos el área y los marker
	   	   	   markersFlightCircle.push(flightCircle);
			   totalResultsFlight += 1;
			}
		   }
	 }
      }
   });
}

