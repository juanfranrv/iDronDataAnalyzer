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
		 $('#paginador').html(
		    function(){
			var content = '<table class="table table-striped"><thead><tr><th>Date</th><th>Temp.</th><th>A. Pressure</th><th>Wind</th><th>Humidity</th><th><p style="visibility:hidden">Delete</p></th></tr></thead><tbody id="myTableBody">';

			if(data.length == 0)
				content = content + '<tr><td>No data found.</td><td></td><td></td><td></td><td></td>';

			for(var i = 0; i < data.length; i++){
			      content = content+'<tr><td style="font-size:14px;">' + data[i].fecha + ' UTC</td>';
			      content = content + '<td style="font-size:16px;">' + data[i].temperatura + ' ºC</td>';
			      content = content + '<td style="font-size:16px;">' + data[i].presion + ' hPa</td>';
			      content = content + '<td style="font-size:16px;">' + data[i].vel_viento + ' kph - ' + data[i].dir_viento + ' º</td>';
			      content = content + '<td style="font-size:16px;">' + data[i].humedad + '%</td>';
			      content = content + '<td><button id="button-' + data[i].id + '" class="btn btn-danger borrarBoton" data-item="' + data[i].id + '" type="submit"><i class="fa fa-trash"></i> Delete</button></td>';

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
			content = content + '<div class="col-md-12 text-center"><ul class="pagination pagination-lg pager" id="myPager"></ul></div>';

			return content;
		    }
		)

		//Paginamos la tabla cada vez que nos la traemos. 8 elementos por página
 		$('#myTableBody').pageMe({pagerSelector:'#myPager',showPrevNext:true,hidePageNumbers:false,perPage:8});
	  }
  });

}

//Iniciliza el freeow (alerta)
$(document).ready(function() {
	opts = {};
	opts.classes = ["gray"];
	opts.classes.push("pushpin");
	opts.autoHide = true;
	opts.showStyle = {
		opacity: 1,
		left: 0
	};
});

$(document).on('click', ".borrarBoton", function () {

	var catid = $(this).attr("data-item")

	if (confirm("Are you sure?")) {
		$.ajax({				//Borramos por id de botón el item elegido por el usuario, utilizando AJAX para llamar al servidor
			type: 'GET',
			url: '/deleteStatistic?id=' + catid,
			data: $(this).serialize(),
			dataType: 'json',
			success: function (data) {
				loadAjax(window.fecha, window.tiempo);	
			}
	  	});

		//Muestra alerta cuando el usuario ha borrado el dato para informarle
		$("#freeow-tr").freeow("Alert", "Data has been deleted successfully", opts);
	}
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

//Paginación de la tabla. 

$.fn.pageMe = function(opts){
	var $this = this,
        defaults = {
            perPage: 7,
            showPrevNext: false,
            hidePageNumbers: false
        },
        settings = $.extend(defaults, opts);

	var listElement = $this;
	var perPage = settings.perPage; 
	var children = listElement.children();
	var pager = $('.pager');

	if (typeof settings.childSelector!="undefined") {
		children = listElement.find(settings.childSelector);
	}

	if (typeof settings.pagerSelector!="undefined") {
		pager = $(settings.pagerSelector);
	}

	var numItems = children.size();
	var numPages = Math.ceil(numItems/perPage);

	pager.data("curr",0);

	if (settings.showPrevNext){
		$('<li><a href="#" class="prev_link">«</a></li>').appendTo(pager);
	}

	var curr = 0;
	while(numPages > curr && (settings.hidePageNumbers==false)){
		$('<li><a href="#" class="page_link">'+(curr+1)+'</a></li>').appendTo(pager);
		curr++;
	}

	if (settings.showPrevNext){
		$('<li><a href="#" class="next_link">»</a></li>').appendTo(pager);
	}

	pager.find('.page_link:first').addClass('active');
	pager.find('.prev_link').hide();
	if (numPages<=1) {
		pager.find('.next_link').hide();
	}
	pager.children().eq(1).addClass("active");

	children.hide();
	children.slice(0, perPage).show();

	pager.find('li .page_link').click(function(){
		var clickedPage = $(this).html().valueOf()-1;
		goTo(clickedPage,perPage);
		return false;
	});
	pager.find('li .prev_link').click(function(){
		previous();
		return false;
	});
	pager.find('li .next_link').click(function(){
		next();
		return false;
	});

	function previous(){
		var goToPage = parseInt(pager.data("curr")) - 1;
		goTo(goToPage);
	}

	function next(){
		goToPage = parseInt(pager.data("curr")) + 1;
		goTo(goToPage);
	}

	function goTo(page){
		var startAt = page * perPage,
		    endOn = startAt + perPage;

		children.css('display','none').slice(startAt, endOn).show();

		if (page>=1) {
		    pager.find('.prev_link').show();
		}
		else {
		    pager.find('.prev_link').hide();
		}

		if (page<(numPages-1)) {
		    pager.find('.next_link').show();
		}
		else {
		    pager.find('.next_link').hide();
		}

		pager.data("curr",page);
		pager.children().removeClass("active");
		pager.children().eq(page+1).addClass("active");

    }
};




