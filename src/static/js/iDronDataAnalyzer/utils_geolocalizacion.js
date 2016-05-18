//------------------------------------------JAVASCRIPT PARA EL TEMPLATE GEOLOCALIZACIÓN----------------------------------------------

//--------------------------------CONFIGURACIÓN GOOGLE MAPS--------------------------------------------------------------------------

var coordenadas;
var marker;
var map;
var markers = [], markersFlight = [], markersCity = [];				//Array para almacenar cada uno de los marker de las zonas detectadas
var markersCityCircle = [], markersFlightCircle = [], markersCircle = [];	//Array para almacenar las áreas de círculos que simbolizan las zonas prohibidas
var totalResults = 0;								//Variable contador para llevar el número de marker que borraremos al seleccionarlo
var checkboxAirport = false, checkboxCity = false, checkboxFlight = false;	//Variables que indican si cada checkbox ha sido pulsado
var airportDetected = false, flightDetected = false, cityDetected = false;	//Variables que indican si se ha entrado en zona prohibida
var num_CityDetected = [], num_airportDetected = [], num_flightDetected = [];   //Arrays que almacenan las zonas invadidas de cada restricción
var checkboxSound = false;

function actualizarMapa() {
  $.ajax({
        type: 'GET',
        url: '/coordenadas',
        data: $(this).serialize(),
        dataType: 'json',
        success: function (data) {
          var latlng = new google.maps.LatLng(data[0].latitud, data[0].longitud);
          marker.setPosition(latlng);
          map.setCenter(latlng); 

	  if(checkboxAirport == true){
		  // Especificamos la localización, el radio y el tipo de lugar que queremos obtener para que se vaya actualizando a medida que avanza el drone
		  var service = new google.maps.places.PlacesService(map);
		  var request = {
		     location: latlng,
		     radius: 7500,
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
			 	      radius:500
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
			if(num_CityDetected[i] != i)
				num_CityDetected.push(i);	//Almacenamos las poblaciones invadidas en un array
		   }
	  	}
		   
		if(num_CityDetected.length > 0){	//Si el array de poblaciones invadidas no está vacío
			//Recorremos y si alguno ha dejado de ser invadido, lo sacamos del array
			for(var i = 0; i < num_CityDetected.length; i++){
				if(markersCityCircle[i].getBounds().contains(latlng) == false){ 
					num_CityDetected.splice(i,1);
				}
			}

			if(num_CityDetected.length == 0){	//Si finalmente el array de poblaciones invadidas está vacío, eliminamos la alerta
				cityDetected = false;
			}
		}


	  }else{
		num_CityDetected = [];
	  	cityDetected = false;
	  }

	  if(checkboxAirport == true){  //Si el checkbox de aeropuerto está activo, comprobamos si el drone está contenido en el área para informar al usuario
	       for (var i = 0; i < markersCircle.length; i++) {
		   if(markersCircle[i].getBounds().contains(latlng)){
			airportDetected = true;
			if(num_airportDetected[i] != i)
				num_airportDetected.push(i);	//Almacenamos los aeropuertos invadidos en un array
		   }
	       }

	       if(num_airportDetected.length > 0){	//Si el array de aeropuertos invadidos no está vacío
			//Recorremos los aeropuertos invadidos y si alguno ha dejado de ser invadido, lo sacamos del array
			for(var i = 0; i < num_airportDetected.length; i++){
				if(markersCircle[i].getBounds().contains(latlng) == false){ 
					num_airportDetected.splice(i,1);
				}
			}

			if(num_airportDetected.length == 0){	//Si finalmente el array de aeropuertos invadidos está vacío, eliminamos la alerta
				airportDetected = false;
			}
		   }

	  }else{
		num_airportDetected = [];
	  	airportDetected = false;
	  }

	  if(checkboxFlight == true){ //Si el checkbox de detección de aviones está activo, comprobamos si el drone está contenido en el área para informar al usuario
	       for (var i = 0; i < markersFlightCircle.length; i++) {
		   if(markersFlightCircle[i].getBounds().contains(latlng)){
			flightDetected = true;
			if(num_flightDetected[i] != i)
				num_flightDetected.push(i);		//Almacenamos los vuelos invadidos
		   }
	       }

		if(num_flightDetected.length > 0){	//Si el array de vuelos invadidos no está vacío
		//Recorremos los vuelos invadidos y si alguno ha dejado de ser invadido, lo sacamos del array
			for(var i = 0; i < num_flightDetected.length; i++){
				if(markersFlightCircle[i].getBounds().contains(latlng) == false){ 
					num_flightDetected.splice(i,1);
				}
			}

			if(num_flightDetected.length == 0){	//Si finalmente el array de vuelos invadidos está vacío, eliminamos la alerta
				flightDetected = false;
			}
		}

	  }else{
		num_flightDetected = [];
	  	flightDetected = false;
	  }

	 //Recarga de datos si se entra en zona prohibida y cuando recibimos nueva información procedente del dron

	 $('#recargar').html(
	    function(){
		var content = '<div style="float:left;margin-left:5%;"><label>Coordinates:&nbsp; </label><span style="font-size:80%;" class="label label-default">&nbsp;' + data[0].latitud + ', ' + data[0].longitud + '</span></div>';
		content = content + '<div style="float:left; margin-left:10%"><label>Altitude:&nbsp; </label><span style="font-size:80%;" class="label label-default">&nbsp;' + data[0].altura + ' m</span></div>';
		content = content + '<div style="float:left; margin-left:10%;"><label>Speed:&nbsp; </label><span style="font-size:80%;" class="label label-default">&nbsp;' + data[0].velocidad + ' m/s</span></div>';
		
		if (data[0].alert == 1){	//Si se supera los 120m de altitud, informamos al usuario
		   content = content + '<div id="warning"><div class="alert alert-danger"><label>If you are using a drone as a hobby or recreational use:<br/><b><u>You are flying above 120 m. Be careful, it is forbidden!</u></b><br/>Remember: What can not I do with my drone? </label><ul><li>I can not fly in urban areas.</li><li>I can not fly above crowds of people: parks, beaches, wedding...</li><li>I can not fly at night.</li> <li>I can not fly close to airports, aircrafts...</li></ul></div></div>';
		}

		if (flightDetected == true){   //Si se entra en zona prohibida (vuelo detectado), informamos al usuario
		   content = content + '<div id="warning"><div class="alert alert-danger"><label><u>Warning:</u> Restricted Zone - You are flying near a plane.</label></div>';
		}

		if (airportDetected == true){   //Si se entra en zona prohibida (aeropuerto detectado), informamos al usuario
		   content = content + '<div id="warning"><div class="alert alert-danger"><label><u>Warning:</u> Restricted Zone - You are flying near an airport.</label></div>';
		}

		if (cityDetected == true){      //Si se entra en zona prohibida (ciudad detectada), informamos al usuario
		   content = content + '<div id="warning"><div class="alert alert-danger"><label><u>Warning:</u> Restricted Zone - You are flying near a populated place.</label></div>';
		}
		
		//Activa sonido cuando hay una alerta
		if(checkboxSound == true){
			if(data[0].alert ==1 || flightDetected == true || airportDetected == true || cityDetected == true){
				   content = content + '<audio id="myAudio" style="display:None" controls autoplay><source src="../static/sound/beep.mp3" type="audio/mpeg"></audio>';
			}	
		}

		return content;
	    }
	)
       }
   });

}

function initialize() {

	var myLatlng;

	$.ajax({
	  type: 'GET',			//Obtiene la latitud y longitud inicial para posicionar el drone. Llamada AJAX al servidor.
	  url: '/coordenadas',
	  data: $(this).serialize(),
	  dataType: 'json',
	  success: function (data) {
		myLatlng = new google.maps.LatLng(data[0].latitud, data[0].longitud);
	  }
	});


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


//------------------------------ACTUALIZACIÓN DINÁMICA DE DETECCIÓN DE ZONAS PROHIBIDAS--------------------------------------------------------------------

$('#airport').change(function() { 
   	if($("#airport").is(':checked')){				//Si la checkbox está seleccionada
	    checkboxAirport = true;
	} else {							//Si la checkbox no está seleccionada
	    checkboxAirport = false;
	}
});

$('#sound').change(function() { 
   	if($("#sound").is(':checked')){				//Si la checkbox está seleccionada
	    checkboxSound = true;
	} else {							//Si la checkbox no está seleccionada
	    checkboxSound = false;
	}
});

$('#city').change(function() { 
   	if($("#city").is(':checked')){					  //Si la checkbox está seleccionada
              checkboxCity = true;
	      activarDeteccionCiudades();

	      intervalCity = setInterval(activarDeteccionCiudades,120000); //Vamos actualizando las ciudades a medida que el drone va avanzando (cada 2 minutos)
	
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

	           for (var i = 0; i < markersCity.length; i++) {		      //Borra todos los marker de ciudades del mapa
	              markersCity[i].setMap(null);
		      markersCityCircle[i].setMap(null);
	           } 

	           markersCity = [];
	           markersCityCircle =[];
	
	  	   for (var i = 0; i < data.length; i++) {

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
			 	      radius:2500
			   });

	   	   	   markersCity.push(markerCity);				//Lo añadimos a cada array para borrarlo cuando el usuario lo seleccione
	   	   	   markersCityCircle.push(PopulationCircle);
			
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
		   }
	   }
      }
   });
}

