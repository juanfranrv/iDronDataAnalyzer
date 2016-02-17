

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
    zoom: 18,
    center: myLatlng
  }
  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
  marker = new google.maps.Marker({
      position: myLatlng,
      map: map,
      title: 'Map',
      icon: '../static/images/dron_geo.png'
  });
}
google.maps.event.addDomListener(window, 'load', initialize);
setInterval(actualizarMapa, 1000);


//------------------------------------------JAVASCRIPT PARA EL TEMPLATE EDITAR_PERFIL Y REGISTRO----------------------------------------------


function seguridad() { // Seguridad para contraseñas
   var longitud = document.getElementById('strength');
   var longitud_alta = new RegExp("^(?=.{8,})(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*\\W).*$", "g");
   var longitud_mediana = new RegExp("^(?=.{7,})(((?=.*[A-Z])(?=.*[a-z]))|((?=.*[A-Z])(?=.*[0-9]))|((?=.*[a-z])(?=.*[0-9]))).*$", "g");
   var password = document.getElementById("password").value;

   if (longitud_alta.test(password)) {
      longitud.innerHTML = '<span style="color:green">Contraseña muy segura</span>';
   } else if (longitud_mediana.test(password)) {
      longitud.innerHTML = '<span style="color:orange">Contraseña normal</span>';
   } else {
    longitud.innerHTML = '<span style="color:red">Contraseña débil</span>';
   }

}


//------------------------------------------JAVASCRIPT PARA EL TEMPLATE REGISTRO----------------------------------------------
	

function Valida(form) {

	var usuario = document.getElementById("usuario").value;
	var password= document.getElementById("password").value;
	var nombre= document.getElementById("nombre").value;
	var apellido= document.getElementById("apellido").value;
	var email= document.getElementById("correo").value;
	var telefono= document.getElementById("telefono").value;
	
		
	  if(usuario.length==0) { //¿Tiene 0 caracteres?
	    alert('No has escrito el nombre de usuario'); //Mostramos el mensaje
	
	    return false; 
	  }

	  if(password.length==0) { //¿Tiene 0 caracteres?
	    alert('No has escrito la contraseña'); //Mostramos el mensaje
	
	    return false; 
	  }
	  if(email.length==0) { //comprueba que no esté vacío
	  
	    alert('No has escrito tu e-Mail');
	    return false;
	  }
	  if(telefono.length==0) { //comprueba que no esté vacío
	  
	    alert('No has escrito tu teléfono');
	    return false;
	  }
	  
	  if( !(/^\d{9}$/.test(telefono)) ) {
	   alert('No has introducido un número de teléfono correcto');
		return false;
	  }
	  
	  if( !(/^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,3})$/.test(email)) ) {
		alert('El formato de email introducido no es el correcto');
		return false;
	  }  
	
	  return true; //Si ha llegado hasta aquí, es que todo es correcto

}


//------------------------------------------JAVASCRIPT PARA EL TEMPLATE LOGIN----------------------------------------------
  

function Valida_login(form) {

	var usuario = document.getElementById("user").value;
	var password= document.getElementById("pass").value;

	if(usuario.length==0) { //¿Tiene 0 caracteres?
		alert('No has escrito el nombre de usuario'); //Mostramos el mensaje
		return false; 
	}

	if(password.length==0) { //comprueba que no esté vacío
		alert('No has escrito tu contraseña');
		return false;
	}

	return true; //Si ha llegado hasta aquí, es que todo es correcto

}


//------------------------------------------JAVASCRIPT PARA EL TEMPLATE PRONÓSTICO----------------------------------------------


 function Valida_pronostico(form) {

	  var latitud = document.getElementById("latitud").value;
	  var longitud = document.getElementById("longitud").value;
		
	  if(latitud.length == 0) { //¿Tiene 0 caracteres?
	  	alert('Introduce latitud'); //Mostramos el mensaje
	        return false; 
	  }

	  if(longitud.length == 0) { //¿Tiene 0 caracteres?
	  	alert('Introduce longitud'); //Mostramos el mensaje
	  	return false; 
	  }
	
	  return true; 

 }
	  

