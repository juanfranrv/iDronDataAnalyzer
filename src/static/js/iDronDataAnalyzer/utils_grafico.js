
//------------------------------------------JAVASCRIPT PARA EL TEMPLATE GRÁFICO (HIGHCHARTS)----------------------------------------------

/**
 * Dark theme for Highcharts JS
 */
// Load the fonts
Highcharts.createElement('link', {
   href: 'http://fonts.googleapis.com/css?family=Unica+One',
   rel: 'stylesheet',
   type: 'text/css'
}, null, document.getElementsByTagName('head')[0]);
Highcharts.theme = {
   colors: ["#e50000", "#2b908f", "#90ee7e", "#f45b5b", "#7798BF", "#aaeeee", "#ff0066", "#eeaaee",
      "#55BF3B", "#DF5353", "#7798BF", "#aaeeee"],
   chart: {
      backgroundColor: {
         linearGradient: { x1: 0, y1: 0, x2: 1, y2: 1 },
         stops: [
            [0, '#2a2a2b'],
            [1, '#3e3e40']
         ]
      },
      style: {
         fontFamily: "'Unica One', sans-serif"
      },
      plotBorderColor: '#606063',
   },
   title: {
      style: {
         color: '#E0E0E3',
         textTransform: 'uppercase',
         fontSize: '20px'
      }
   },
   subtitle: {
      style: {
         color: '#E0E0E3',
         textTransform: 'uppercase'
      }
   },
   xAxis: {
      gridLineColor: '#707073',
      labels: {
         style: {
            color: '#E0E0E3'
         }
      },
      lineColor: '#707073',
      minorGridLineColor: '#505053',
      tickColor: '#707073',
      title: {
         style: {
            color: '#A0A0A3'
         }
      }
   },
   yAxis: {
      gridLineColor: '#707073',
      labels: {
         style: {
            color: '#E0E0E3'
         }
      },
      lineColor: '#707073',
      minorGridLineColor: '#505053',
      tickColor: '#707073',
      tickWidth: 1,
      title: {
         style: {
            color: '#A0A0A3'
         }
      }
   },
   tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.85)',
      style: {
         color: '#F0F0F0'
      }
   },
   plotOptions: {
      series: {
         dataLabels: {
            color: '#B0B0B3'
         },
         marker: {
            lineColor: '#333'
         }
      },
      boxplot: {
         fillColor: '#505053'
      },
      candlestick: {
         lineColor: 'white'
      },
      errorbar: {
         color: 'white'
      }
   },
   legend: {
      itemStyle: {
         color: '#E0E0E3'
      },
      itemHoverStyle: {
         color: '#FFF'
      },
      itemHiddenStyle: {
         color: '#606063'
      }
   },
   credits: {
      style: {
         color: '#666'
      }
   },
   labels: {
      style: {
         color: '#707073'
      }
   },
   drilldown: {
      activeAxisLabelStyle: {
         color: '#F0F0F3'
      },
      activeDataLabelStyle: {
         color: '#F0F0F3'
      }
   },
   navigation: {
      buttonOptions: {
         symbolStroke: '#DDDDDD',
         theme: {
            fill: '#505053'
         }
      }
   },
   // scroll charts
   rangeSelector: {
      buttonTheme: {
         fill: '#505053',
         stroke: '#000000',
         style: {
            color: '#CCC'
         },
         states: {
            hover: {
               fill: '#707073',
               stroke: '#000000',
               style: {
                  color: 'white'
               }
            },
            select: {
               fill: '#000003',
               stroke: '#000000',
               style: {
                  color: 'white'
               }
            }
         }
      },
      inputBoxBorderColor: '#505053',
      inputStyle: {
         backgroundColor: '#333',
         color: 'silver'
      },
      labelStyle: {
         color: 'silver'
      }
   },
   navigator: {
      handles: {
         backgroundColor: '#666',
         borderColor: '#AAA'
      },
      outlineColor: '#CCC',
      maskFill: 'rgba(255,255,255,0.1)',
      series: {
         color: '#7798BF',
         lineColor: '#A6C7ED'
      },
      xAxis: {
         gridLineColor: '#505053'
      }
   },
   scrollbar: {
      barBackgroundColor: '#808083',
      barBorderColor: '#808083',
      buttonArrowColor: '#CCC',
      buttonBackgroundColor: '#606063',
      buttonBorderColor: '#606063',
      rifleColor: '#FFF',
      trackBackgroundColor: '#404043',
      trackBorderColor: '#404043'
   },
   // special colors for some of the
   legendBackgroundColor: 'rgba(0, 0, 0, 0.5)',
   background2: '#505053',
   dataLabelsColor: '#B0B0B3',
   textColor: '#C0C0C0',
   contrastTextColor: '#F0F0F3',
   maskColor: 'rgba(255,255,255,0.3)'
};
// Apply the theme
Highcharts.setOptions(Highcharts.theme);
$(function () {
    var charts;
    $(document).ready(function () {
        Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });
          var num;
          function callAjax() {
            $.ajax({
                          type: 'GET',
			  //Enviamos por url el dato a mostrar en el gráfico y si se ha elegido guardar para almacenar la información
                          url: '/datos_grafico?dato=' + getDato() + '&save=' + getSave(),  
                          data: $(this).serialize(),
                          dataType: 'json',
                          success: function (data) {

				  if(getSave() == true)		//Si se ha enviado la activación de Guardar, actualizamos a False para no guardar más datos
  				  	setSave(false);

				  //Si el servicio web da error, informamos al usuario, en caso contrario mostramos datos
				  if(data == 'Chart web service is temporarily unavailable.'){	

				       $('#fail').html(
					      function(){
						 var content = '<div style="margin-top:50px;"><div class="alert alert-danger"><label><u>Error:  </u>Chart web service is temporarily unavailable.</label></div>';
						  return content;
					      }
				       )

				  }else{

                                 	num = data;
                                  }
                          }
                  });
            return num;
          }
          
          charts = $('#container-temp-grande').highcharts({
            chart: {
                type: document.getElementById('tipoGrafica-temp').value,
                animation: Highcharts.svg, // don't animate in old IE
                marginRight: 10,
                events: {
                    load: function () {
                        // set up the updating of the chart each second
                        var series = this.series[0];
                        setInterval(function () {
                            var x = (new Date()).getTime(), // current time            
                                y = callAjax();
                            series.addPoint([x, y], true, true);
                        }, 1000);
                    }
                },
            },
            title: {
                text: document.getElementById('tipoGrafica-temp1').value
            },
            xAxis: {
		title: {
                    text: 'Current time'
                },
                type: 'datetime',
                text: 'Datetime',
                tickPixelInterval: 150
            },
            yAxis: {
                title: {
                    text: 'Data'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                formatter: function () {
                    return '<b>' + this.series.name + '</b><br/>' +
                        Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                        Highcharts.numberFormat(this.y, 2);
                }
            },
            legend: {
                enabled: false
            },
            exporting: {
                enabled: false
            },
            series: [{
                name: document.getElementById('tipoGrafica-temp1').value,
                data: (function () {
                    // generate an array of random data
                    var data = [],
                        time = (new Date()).getTime(),
                        i;
                    for (i = -19; i <= 0; i += 1) {
                        data.push({
                            x: time + i * 1000,
                            y: 0
                        });
                    }
                    return data;
                }())
            }],
        },
        function (charts) {

            $('#tipoGrafica-temp').change(function () {
                charts.series[0].update({
                    type: document.getElementById('tipoGrafica-temp').value
                });
            });

	    $('#tipoGrafica-temp1').change(function () {
                charts.setTitle({text: document.getElementById('tipoGrafica-temp1').value});
		charts.series[0].update({name: document.getElementById('tipoGrafica-temp1').value}, true);
		var tipo_dato = document.getElementById('tipoGrafica-temp1').value;
		setDato(tipo_dato);
            });

        }); 
        
    });
    
});

//Servicio para enviar los datos desde el change() hasta la función Ajax del highchart y pasarle el valor como argumento a la url para poder enviar un dato u otro

var tipoDatoElegido;
var save = false;

function setDato(tipoAasignar) {
  tipoDatoElegido = tipoAasignar;
}

function getDato() {
  return tipoDatoElegido;
}

///Servicio para guardar información cuando el usuario haya pulsado el botón "Guardar". Manda la información desde el evento "click" hasta el AJAX que realiza la petición más arriba

function setSave(tipo) {
  save = tipo;
}

function getSave() {
  return save;
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

$(document).on('click', "#SaveButton", function () {	//Cuando el usuario pulsa "Guardar", actualizamos la variable a True
    
  setSave(true);

  //Muestra alerta cuando el usuario ha borrado el dato para informarle
  $("#freeow-tr").freeow("Alert", "Weather data has been saved successfully", opts);

});


