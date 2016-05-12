//------------------------------------------JAVASCRIPT PARA EL TEMPLATE ESTADÍSTICAS----------------------------------------------


var checkbox = false;
$("#chart").hide();
var mySeries = [];
var myFechas = [];

//Servicio para obtener o actualizar el clima seleccionado por el usuario
var clima = "temperatura";

function setClima(tipoAasignar) {
	clima = tipoAasignar;
}

function getClima() {
	return clima;
}

//Hace peticiones al servidor para actualizar los datos del gráfico
function loadAjaxClima(){

  $.ajax({
	  type: 'GET',
	  url: '/getDatosAtmosfericos?fecha=' + window.fecha + '&tiempo=' + window.tiempo,
	  data: $(this).serialize(),
	  dataType: 'json',
	  success: function (data) {
		 $('table').html(
		    function(){
			for(var i = 0; i < data.length; i++){
			  myFechas.push([data[i].fecha]);

			  if (checkbox == true){
			      switch(getClima()){
			      	case 'temperatura':
			      		mySeries.push([i, data[i].temperatura]);
					break;
				case 'presion':
			      		mySeries.push([i, data[i].presion]);
					break;
				case 'vel_viento':
			      		mySeries.push([i, data[i].vel_viento]);
					break;
				case 'dir_viento':
			      		mySeries.push([i, data[i].dir_viento]);
					break;
				case 'humedad':
			      		mySeries.push([i, data[i].humedad]);
					break;
			      }
			  }
			}

			load();
			mySeries = [];
			myFechas = [];
		    }
		)
	  }
  });

}

//Hace peticiones al servidor para actualizar los datos del gráfico y tabla
function loadAjax(fecha, tiempo){
  $.ajax({
	  type: 'GET',
	  url: '/getDatosAtmosfericos?fecha=' + fecha + '&tiempo=' + tiempo,
	  data: $(this).serialize(),
	  dataType: 'json',
	  success: function (data) {		//Recarga dinámica de contenido HTML sin actualizar la página
		 $('table').html(
		    function(){
			var content = '<table class="table table-striped"><thead><tr><th>Date</th><th>Temp.</th><th>A. Pressure</th><th>Wind</th><th>Humidity</th><th><p style="visibility:hidden">Delete</p></th></tr></thead><tbody>';

			for(var i = 0; i < data.length; i++){
			      content = content+'<tr><td style="font-size:14px;">' + data[i].fecha + ' UTC</td>';
			      content = content + '<td style="font-size:16px;">' + data[i].temperatura + ' ºC</td>';
			      content = content + '<td style="font-size:16px;">' + data[i].presion + ' hPa</td>';
			      content = content + '<td style="font-size:16px;">' + data[i].vel_viento + ' kph - ' + data[i].dir_viento + ' º</td>';
			      content = content + '<td style="font-size:16px;">' + data[i].humedad + '%</td>';
			      content = content + '<td><button id="button-' + data[i].id + '" class="btn btn-danger borrarBoton" data-item="' + data[i].id + '" type="submit" class="btn btn-danger">Delete</button></td>';

			      myFechas.push([data[i].fecha]);

			      if (checkbox == true){

				      switch(getClima()){
				      	case 'temperatura':
				      		mySeries.push([i, data[i].temperatura]);
						break;
					case 'presion':
				      		mySeries.push([i, data[i].presion]);
						break;
					case 'vel_viento':
				      		mySeries.push([i, data[i].vel_viento]);
						break;
					case 'dir_viento':
				      		mySeries.push([i, data[i].dir_viento]);
						break;
					case 'humedad':
				      		mySeries.push([i, data[i].humedad]);
						break;
				      }
			     }

			}

			load();						//Pintamos el gráfico con los datos del array
			mySeries = [];
			myFechas = [];
			content = content + '</tr></tbody></table>';

			return content;
		    }
		)
	  }
  });

}

$(document).on('click', ".borrarBoton", function () {

	var catid = $(this).attr("data-item")

	$.ajax({
		type: 'GET',
		url: '/deleteStatistic?id=' + catid,
		data: $(this).serialize(),
		dataType: 'json',
		success: function (data) {
			loadAjax(window.fecha, window.tiempo);	
		}
  	});

 	loadAjax(window.fecha, window.tiempo);	
});

//Si la checkbox cambia, dependiendo de si está seleccionada o no, vamos a proceder a mostrar el gráfico y su select asociado
$('#afirmar').change(function() { 
   	if($("#afirmar").is(':checked')){				//Si la checkbox está seleccionada

	    $("#data_grafico").show();					//Mostramos los dos select asociados y el gráfico
	    $("#shape_grafico").show();
	    $("#chart").show();
	    checkbox = true;

  	    loadAjaxClima();

	} else {							//Si la checkbox no está seleccionada

	    $("#data_grafico").hide();					
	    $("#shape_grafico").hide();					//Escondemos los select asociados y el gráfico
	    $("#chart").hide();
	    checkbox = false;
	}
});

$('#data_grafico').change(function () {			//Evento que obtiene el tipo de dato a mostrar en el gráfico y actualiza este

	var dato_clima = document.getElementById('data_grafico').value;
	setClima(dato_clima);

	loadAjaxClima();
});

$('#shape_grafico').change(function () {			//Evento que obtiene el tipo de dato a mostrar en el gráfico y actualiza este

	var forma_grafico = document.getElementById('shape_grafico').value;
	window.forma = forma_grafico;

  	loadAjaxClima();
});

$('#tiempo').change(function(){			//Select asociado al tiempo

	var tipo_tiempo = document.getElementById('tiempo').value;
	window.tiempo = tipo_tiempo;     		//Almacenamos la variable para poder usarla en el evento de abajo

	loadAjax(window.fecha, tipo_tiempo);

});

$('#datepicker').change(function () {		//Actualiza los datos al cambiar de fecha,sin recargar la página, utilizando AJAX

	var tipo_dato = document.getElementById('datepicker').value;
	window.fecha = tipo_dato;

	loadAjax(tipo_dato, window.tiempo);

});

$(document).ready(				//Lanza la selección de fecha
	function () {
	    $( "#datepicker" ).datepicker({
	      dateFormat: "dd-mm-yy",
	      changeMonth: true,
	      changeYear: true 
	    });
	}
);

//GRÁFICO HIGHCHART DE ESTADÍSTICAS

function load(){
	var chart = new Highcharts.Chart({
		chart: {
			renderTo: 'chart',
			type: 'column',
			margin: 75,
			marginTop:100,
			options3d: {
				enabled: true,
				alpha: 0,
				beta: 0,
				depth: 50,
				viewDistance: 25
			}
		},
		title: {
			text: '',
		},
		subtitle: {
			text: ''
		},

		xAxis: {
		      categories: myFechas,
		      labels: {
			 style: {
			    fontSize:'9px'
			 }
		      }
		},

		scrollbar: { enabled: true },

		yAxis: {
			allowDecimals: false,
			min: 0,
			max: 1000,
			title: {
				text: 'ºC'
			}
		},
		plotOptions: {
			column: {
				depth: 25
			}
		},
		legend: {
		    layout: 'vertical',
		    align: 'left',
		    x: 600,
		    verticalAlign: 'top',
		    y: 40,
		    floating: true,
		    backgroundColor: '#FFFFFF'
		},
		series: [{ 
		    name: 'Temperatura',
		    data: mySeries
		}]
	});

	switch(getClima()){			//Dependiendo del dato atmosférico seleccionado vamos cambiando los valores

		case 'temperatura':		//Cambios dinámicos de extremos, título y nombre de series tanto para presión como para temperatura
		     chart.yAxis[0].setExtremes(0, 50);
		     chart.yAxis[0].axisTitle.attr({
			text: 'ºC'
		     });
		     chart.series[0].update({name:"Temperature"}, false);
		     chart.redraw();
		     break;

		case 'presion':
		     chart.yAxis[0].setExtremes(0, 1500);
		     chart.yAxis[0].axisTitle.attr({
			text: 'hPa'
		     });
		     chart.series[0].update({name:"Atmospheric pressure"}, false);
		     chart.redraw();
		     break;

		case'vel_viento':
		     chart.yAxis[0].setExtremes(0, 50);
		     chart.yAxis[0].axisTitle.attr({
			text: 'kph'
		     });
		     chart.series[0].update({name:"Wind speed"}, false);
		     chart.redraw();
		     break;

		case 'dir_viento':
		     chart.yAxis[0].setExtremes(0, 360);
		     chart.yAxis[0].axisTitle.attr({
			text: 'º'
		     });
		     chart.series[0].update({name:"Wind direction"}, false);
		     chart.redraw();
		     break;

		case 'humedad':
		     chart.yAxis[0].setExtremes(0, 100);
		     chart.yAxis[0].axisTitle.attr({
			text: '%'
		     });
		     chart.series[0].update({name:"Humidity"}, false);
		     chart.redraw();
		     break;
	}

	if(window.forma == 'spline'){	//Si la forma "Línea" está seleccionada, pintamos el gráfico con dicha forma. En caso contrario, como columna 3D
	     chart.series[0].update({
		type: window.forma
	     });
	}

}
