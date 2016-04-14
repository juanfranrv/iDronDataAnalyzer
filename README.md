# iDronDataAnalyzer 

##Aplicación que gestiona la seguridad para drones##

### Proyecto de fin de grado UGR || Talentum Telefónica ###

Se pronostica que se va a proceder a invertir en drones más de 100.000 millones de dólares en 5 años aprox. Sin embargo, no se disponen de aplicaciones destinadas a la seguridad para drones en las que se muestre el avance del drone y las medidas de seguridad simultáneamente. 

Debido a la no disponibilidad de estas aplicaciones, se están produciendo numerosas incidencias entre drones y aviones, entre otras. Este sistema pretende solucionar dichos problemas:

* Captura de información: Cuando un drone está en movimiento, es necesario tener una serie de personas encargadas de estudiar y observar los diversos datos que presenta la zona por la que va circulando, como la humedad, la temperatura, la velocidad del viento o la trayectoria, que son datos necesarios para decidir, por ejemplo, si cambiar la trayectoria del drone o ver si está en peligro. Para realizar estas tareas sería de gran utilidad la disposición de un sistema web que nos permita monitorizar y analizar dichos datos de suma importancia para el desarrollo con éxito de la misión.

* Seguridad: El sistema gestionará varios aspectos en el tema de "Seguridad para drones" que la mayoría de los usuarios desconoce, como es el acceso prohibido a aeropuertos, a poblaciones, áreas donde haya vuelo aéreo frecuente... El drone detectará automáticamente estas zonas informando de que se encuentra en área restringida.

***

### Requisitos de la aplicación ###

La aplicación tendrá que cumplir los siguientes requisitos:

* [X] Monitorización y análisis de datos atmosféricos en tiempo real.  
* [X] Seguimiento del drone utilizando el GPS incorporado. Además, se mostrarán los aeropuertos más cercanos (zona prohibida) y se podrá consultar la altura del terreno por el que va circulando el drone.
* [X] Pronóstico de datos atmosféricos por horas o por días.
* [X] Almacenamiento de datos monitorizados para el posterior estudio de la misión. Estudio con gráficos.
* [X] Detección de los datos atmosféricos procedentes del METAR y TAF del aeropuerto más cercano por el que vaya circulando el drone en ese momento.
* [ ] Detección de tráfico aéreo y/o fronteras con poblaciones (zonas restringidas).
 
***

### Conexión con drone ###

Como el servidor no deja añadir las librerías de comunicación con el drone (como por ejemplo Dronekit), he decidido crear una aplicación Android que haga de "proxy" entre el drone y el servidor. Esta app va a gestionar todo lo relacionado con el drone (conexión, telemetría...) y la va a mandar al servidor donde será procesada en tiempo real. 

Por otro lado, el servidor permanecerá ajeno de todo lo relacionado con el drone. Se encargará de recibir la información mandada por la aplicación de Android y utilizarla para cada una de sus funcionalidades.

***

### Instalación: ###

Actualizamos repositorios:

    sudo apt-get update
    
Instalamos python y sus dependencias:

    apt-get -y install python python-setuptools build-essential python-dev
    easy_install pip
    
Instalamos git y clonamos el repositorio:

    apt-get install -y git
    git clone https://github.com/juanfranrv/iDronDataAnalyzer.git

Descargamos e iniciamos los módulos del SDK de Google App Engine y lanzamos el demonio del sistema:

    cd iDronDataAnalyzer && \
    git submodule init && \
    git submodule sync && \
    git submodule update && \
    chmod 755 install.sh && \
    sudo ./install.sh
    
***

### Desinstalación: ###

Lanzamos el script con permisos de ejecución:

    sudo ./uninstall.sh


***

### Parar y lanzar servicio: ###

Para lanzar el servicio:

    sudo service iDronDataAnalyzer start

Para parar el servicio:s

    sudo service iDronDataAnalyzer stop 
    
***

### Contenedor Docker para lanzar e instalar toda la aplicación automáticamente: ###

[Visitar sitio Docker con el contenedor de la aplicación](https://hub.docker.com/r/juanfranrv/idrondataanalyzer/)

    sudo docker pull juanfranrv/idrondataanalyzer

    
### Para desplegar la aplicación en la nube automáticamente: ###

Dar permisos y ejecutar el script [deployToGAE.sh](https://github.com/juanfranrv/iDronDataAnalyzer/blob/master/deployToGAE.sh). Inmediatamente, tendremos la aplicación desplegada en la nube de Google App Engine.

***

### Para lanzar el simulador del drone: ###

1. Lanzar el script [dronekit.sh](https://github.com/juanfranrv/iDronDataAnalyzer/blob/master/dronekit.sh). Instalará las dependencias necesarias y lanzará un simulador de tipo drone.

2. Lanzar el script [mavproxy.sh](https://github.com/juanfranrv/iDronDataAnalyzer/blob/master/mavproxy.sh). De esta forma, tendremos el proxy activado para interpretar los mensajes MAVLINK que vamos a enviar al drone. Este proxy se conectará al drone simulado en el paso anterior.

3. Ejecutar el script de python [vehicle_state.py](https://github.com/juanfranrv/iDronDataAnalyzer/blob/master/src/iDronDataAnalyzer/vehicle_state.py) para comprobar que se muestran los datos deseados obtenidos del drone simulado.

***

### Noticias interesantes: ###

Incidencias de drones con aviones en zonas restringidas:

* [Noticia 1](http://economia.elpais.com/economia/2016/03/02/actualidad/1456911759_020181.html)
* [Noticia 2](http://economia.elpais.com/economia/2016/03/04/actualidad/1457078339_462092.html)
* [Noticia 3](http://www.elmundo.es/internacional/2016/03/04/56d93e71e2704e3d4c8b45f6.html)

Los problemas con drones en las noticias anteriores, han ocurrido por la no disposición de suficientes aplicaciones que traten la seguridad para drones. Esta aplicación intentará solucionar dichos problemas.




