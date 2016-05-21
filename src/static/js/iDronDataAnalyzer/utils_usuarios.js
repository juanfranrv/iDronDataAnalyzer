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
		$.ajax({			//Borramos por id de boton el item elegido por el usuario, utilizando AJAX para llamar al servidor
			type: 'GET',
			url: '/deleteUsuario?id=' + catid,
			data: $(this).serialize(),
			dataType: 'json',
			success: function (data) {
				loadAjaxUsuarios();	
			}
	  	});

		//Muestra alerta cuando el usuario ha borrado el dato para informarle
		$("#freeow-tr").freeow("Alert", "User has been deleted successfully", opts)
	}	
});

$(document).on('click', ".editarBoton", function () {

	var editID = $(this).attr("data-item")
	location.href= '/editar_perfil?id=' + editID;
});

//Hace peticiones al servidor para actualizar los datos del gráfico y tabla
function loadAjaxUsuarios(){
  $.ajax({
	  type: 'GET',
	  url: '/getUsuarios',
	  data: $(this).serialize(),
	  dataType: 'json',
	  success: function (data) {		//Recarga dinámica de contenido HTML sin actualizar la página
		 $('#paginador').html(
		    function(){
			var content = '<table class="table table-striped table-hover"><thead><tr><th>User Information</th><th></th><th></th><th></th><th></th><th></th><th></th><th></th></tr></thead><tbody id="myTableBody">';

			if(data.length == 0)
				content = content + '<tr><td>No user found.</td><td></td><td></td><td></td><td></td>';

			for(var i = 0; i < data.length; i++){
			      content = content+'<tr><td style="font-size:14px;"><b>' + data[i].usuario + '</b></td>';
			      content = content + '<td style="font-size:16px;">' + data[i].password + '</td>';
			      content = content + '<td style="font-size:16px;">' + data[i].nombre + '</td>';
			      content = content + '<td style="font-size:16px;">' + data[i].apellido + '</td>';
			      content = content + '<td style="font-size:16px;">' + data[i].correo + '</td>';
			      content = content + '<td style="font-size:16px;">' + data[i].telefono + '</td>';
			      content = content + '<td style="font-size:16px;">' + data[i].tipo + '</td>';
			      content = content + '<td><button id="button-' + data[i].id + '" class="btn btn-warning editarBoton" data-item="' + data[i].id + '" type="submit"> Edit</button><button style="margin-left:5%;" id="button-' + data[i].id + '" class="btn btn-danger borrarBoton" data-item="' + data[i].id + '" type="submit"><i class="fa fa-trash"></i></button></td>';
			}

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

loadAjaxUsuarios();

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

$(document).ready(function(){
	$('#myTableBody').pageMe({pagerSelector:'#myPager',showPrevNext:true,hidePageNumbers:false,perPage:8});
});
