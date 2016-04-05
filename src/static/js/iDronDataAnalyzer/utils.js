//------------------------------------------JAVASCRIPT PARA EL TEMPLATE EDITAR_PERFIL Y REGISTRO----------------------------------------------


function seguridad() { // Seguridad para contraseñas
   var longitud = document.getElementById('strength');
   var longitud_alta = new RegExp("^(?=.{8,})(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*\\W).*$", "g");
   var longitud_mediana = new RegExp("^(?=.{7,})(((?=.*[A-Z])(?=.*[a-z]))|((?=.*[A-Z])(?=.*[0-9]))|((?=.*[a-z])(?=.*[0-9]))).*$", "g");
   var password = document.getElementById("password").value;

   if (longitud_alta.test(password)) {
      longitud.innerHTML = '<span style="color:green">Secure password</span>';
   } else if (longitud_mediana.test(password)) {
      longitud.innerHTML = '<span style="color:orange">Normal password</span>';
   } else {
    longitud.innerHTML = '<span style="color:red">Weak password</span>';
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
	    alert('Insert username'); //Mostramos el mensaje
	
	    return false; 
	  }

	  if(password.length==0) { //¿Tiene 0 caracteres?
	    alert('Insert password'); //Mostramos el mensaje
	
	    return false; 
	  }
	  if(email.length==0) { //comprueba que no esté vacío
	  
	    alert('Insert email');
	    return false;
	  }
	  if(telefono.length==0) { //comprueba que no esté vacío
	  
	    alert('Insert phone');
	    return false;
	  }
	  
	  if( !(/^\d{9}$/.test(telefono)) ) {
	   alert('Insert a valid phone');
		return false;
	  }
	  
	  if( !(/^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,3})$/.test(email)) ) {
		alert('Insert a valid email');
		return false;
	  }  
	
	  return true; //Si ha llegado hasta aquí, es que todo es correcto

}


//------------------------------------------JAVASCRIPT PARA EL TEMPLATE LOGIN----------------------------------------------
  

function Valida_login(form) {

	var usuario = document.getElementById("user").value;
	var password= document.getElementById("pass").value;

	if(usuario.length==0) { //¿Tiene 0 caracteres?
		alert('Insert username'); //Mostramos el mensaje
		return false; 
	}

	if(password.length==0) { //comprueba que no esté vacío
		alert('Insert password');
		return false;
	}

	return true; //Si ha llegado hasta aquí, es que todo es correcto

}


//------------------------------------------JAVASCRIPT PARA EL TEMPLATE PRONÓSTICO----------------------------------------------


 function Valida_pronostico(form) {

	  var latitud = document.getElementById("latitud").value;
	  var longitud = document.getElementById("longitud").value;
		
	  if(latitud.length == 0) { //¿Tiene 0 caracteres?
	  	alert('Insert latitude'); //Mostramos el mensaje
	        return false; 
	  }

	  if(longitud.length == 0) { //¿Tiene 0 caracteres?
	  	alert('Insert longitude'); //Mostramos el mensaje
	  	return false; 
	  }
	
	  return true; 

 }
	  

