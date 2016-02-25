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


