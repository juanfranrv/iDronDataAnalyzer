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
	    alert('Enter username'); //Mostramos el mensaje
	
	    return false; 
	  }

	  if(password.length==0) { //¿Tiene 0 caracteres?
	    alert('Enter password'); //Mostramos el mensaje
	
	    return false; 
	  }
	  if(email.length==0) { //comprueba que no esté vacío
	  
	    alert('Enter email');
	    return false;
	  }
	  if(telefono.length==0) { //comprueba que no esté vacío
	  
	    alert('Enter phone');
	    return false;
	  }
	  
	  if( !(/^\d{9}$/.test(telefono)) ) {
	   alert('Enter a valid phone');
		return false;
	  }
	  
	  if( !(/^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,3})$/.test(email)) ) {
		alert('Enter a valid email');
		return false;
	  }  
	
	  return true; //Si ha llegado hasta aquí, es que todo es correcto

}


//------------------------------------------JAVASCRIPT PARA EL TEMPLATE LOGIN----------------------------------------------
  

function Valida_login(form) {

	var usuario = document.getElementById("user").value;
	var password= document.getElementById("pass").value;

	if(usuario.length==0) { //¿Tiene 0 caracteres?
		alert('Enter username'); //Mostramos el mensaje
		return false; 
	}

	if(password.length==0) { //comprueba que no esté vacío
		alert('Enter password');
		return false;
	}

	return true; //Si ha llegado hasta aquí, es que todo es correcto

}


//------------------------------------------JAVASCRIPT PARA EL TEMPLATE PRONÓSTICO----------------------------------------------


 function Valida_pronostico(form) {

	  var latitud = document.getElementById("latitud").value;
	  var longitud = document.getElementById("longitud").value;
		
	  if(latitud.length == 0) { //¿Tiene 0 caracteres?
	  	alert('Enter latitude'); //Mostramos el mensaje
	        return false; 
	  }

	  if(longitud.length == 0) { //¿Tiene 0 caracteres?
	  	alert('Enter longitude'); //Mostramos el mensaje
	  	return false; 
	  }
	
	  return true; 

 }
	  

