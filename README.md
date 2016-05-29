# iDronDataAnalyzer [![Run Status](https://api.shippable.com/projects/570f55402a8192902e1c084c/badge?branch=master)](https://app.shippable.com/projects/570f55402a8192902e1c084c)

##Aplicación que gestiona la seguridad para drones##

### Proyecto de fin de grado UGR || Talentum Telefónica ###

Los drones están siendo noticia en todo el mundo, tanto por su uso bélico como también en el área de la ciencia y ayuda a la humanidad. Esta tecnología, sin tripulación, es cada vez más común. Se pronostica que se va a invertir en este área más de 100.000 millones de dólares en los próximos 5 años. 

El término correcto para referirse a ellos es UAV (Vehículo Aéreo no Tripulado) y mezclan lo más avanzado en el campo de la aeronáutica y la robótica, logrando acciones que ningún humano podría realizar. Son utilizados en tareas de diversa índole, es decir, desde tareas que pueden ser peligrosas para una persona hasta tareas que requieren un nivel de exactitud que solo logra la tecnología.

A pesar de las numerosas ventajas, existen problemas provocados por el uso de esta tecnología, como por ejemplo incidentes con aviones, inclusiones en aeropuertos o aeródromos... Cada país dispone de una legislación propia para drones que todos los usuarios deberían de conocer y cumplir. Sin embargo, los drones suelen volar donde no deben, pudiendo provocar conflictos y situaciones de riesgo. Los pilotos y operadores de drones no siguen la normativa, y los cuerpos de seguridad del Estado, muchas veces la desconocen y no saben cómo actuar.

En este proyecto se propone la solución de los problemas anteriores mediante la implementación de un sistema alojado en la nube cuyo objetivo consiste en informar al usuario sobre diversos aspectos relacionados con la seguridad de estos vehículos y en la captura de información meteorológica para poder volar de forma óptima. De esta forma, el usuario podrá volar su dron sin miedo a sanciones o poner en peligro a otras aeronaves o infraestructuras.

***

### Requisitos de la aplicación ###

La aplicación tendrá que cumplir los siguientes requisitos:

* [X] Monitorización y análisis de datos atmosféricos en tiempo real.  
* [X] Seguimiento del drone utilizando el GPS incorporado. Además, se mostrarán las zonas restringidas en el área por la que vaya circulando el dron: como aeropuertos o aeródromos más cercanos, núcleos urbanos o tráfico aéreo, alertando tanto por mensaje como por sonido si se invade alguna de ellas. Se podrá consultar la altura del terreno por el que va circulando el dron y la salida/puesta de sol (prohibición de circular por la noche).
* [X] Pronóstico de datos atmosféricos por horas o por días.
* [X] Almacenamiento de datos monitorizados para el posterior estudio de la misión. Estudio con gráficos.
* [X] Detección de los datos atmosféricos procedentes del METAR y TAFOR del aeropuerto más cercano por el que vaya circulando el drone en ese momento.
* [X] Datos como la altura, velocidad y coordenadas del dron estarán actualizados constantemente mientras el dron esté volando.
 
***

### Aplicación Android ###

Para que el servidor obtenga toda la telemetría procedente del dron, es necesario una aplicación Android que haga de "proxy" entre el dron y el servidor. Esta aplicación va a gestionar todo lo relacionado con el drone (conexión, telemetría...) y la va a enviar al servidor donde será procesada en tiempo real. 

Por otro lado, el servidor permanecerá ajeno de todo lo relacionado con el drone. Se encargará de recibir la información mandada por la aplicación de Android y utilizarla para cada una de sus funcionalidades.

La aplicación utiliza la API de [Dronekit](http://dronekit.io/). Esta librería ha sido creada hace menos de un año y permite desarrollar software para cualquier dron cuyo protocolo de comunicación sea MAVLINK. Por lo tanto, con esta librería podemos generalizar nuestra aplicación para que sea válida para cualquier dron fabricado por las grandes empresas del sector.

Para descargar la apk de la aplicación Android, pincha [aquí](https://drive.google.com/open?id=0B2i9UMs9qffmQ212V3h2MDJkUXM)

Enlace al repositorio de la aplicación Android, pincha [aquí](https://github.com/juanfranrv/iDronDataAnalyzer_AndroidApp)

Con esta aplicación podemos conectarnos a nuestro dron tanto por USB como por UDP y obtener toda la telemetría (coordenadas GPS, velocidad, altura a la que circula...). Esta información se irá mandando al servidor constantemente, por lo que podremos acceder a la aplicación web y gestionar todas las funcionalidades con los datos que vayamos obteniendo.

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

***

### Para desplegar la aplicación en la nube automáticamente: ###

Dar permisos y ejecutar el script [deployToGAE.sh](https://github.com/juanfranrv/iDronDataAnalyzer/blob/master/deployToGAE.sh). Inmediatamente, tendremos la aplicación desplegada en la nube de Google App Engine.

***

###Integración contínua con Shippable:###

Con cada commit la aplicación se desplegará de manera automática en Google App Engine (si pasa todos los test) gracias al script [shippale.yml](https://github.com/juanfranrv/iDronDataAnalyzer/blob/master/shippable.yml)

*** 

### Para lanzar el simulador SILT profesional y simular un dron: ###

Primero descargamos Ardupilot:

    git clone https://github.com/ArduPilot/ardupilot
    
Nos situamos en el directorio de ArduPlane o ArduCopter (simuladores) y lanzamos el script:

    sim_vehicle.sh -L GRX --console --map --aircraft test --out 192.168.43.1:14550  

Le indicamos desde que ciudad queremos que despegue (-L GRX). En este caso le he dicho Granada porque lo he predefinido previamente, para ello tenemos que ir a ardupilot/Tools/autotest y en locations.txt añadir las coordenadas que deseemos para el despegue. Como salida de los datos obtenidos (--out 192.168.43.1:14550), le indicamos la dirección UDP que deseemos (en nuestro caso tenemos que estar conectados a la misma red desde nuestro ordenador y desde nuestro dispositivo Android e indicarle la dirección IP de la red a la que está conectada nuestro dispositivo Android para que envíe los datos que reciba) y como puerto 14550 que es el puerto por defecto de escucha de MAVLINK (protocolo de comunicación con el dron). 

Posteriormente, se nos abrirá varias terminales. Dos de ellas meramente informativas y una de ellas para mandar mensajes MAVLINK (veremos 'MANUAL>'). En esta última, vamos a proceder a cargar una misión:
    
    wp load ../Tools/autotest/ArduPlane-Missions/CMAC-toff-loop.txt
    
Esta misión la trae Ardupilot por defecto. Sitúa un dron en Camberra y da vueltas alrededor del aeropuerto de vuelos recreativos. Si queremos modificar la ruta, tenemos que descargar "MissionPlanner" y definir nuestra propia misión.

Posteriormente, le decimos a ArduPlane o ArduCopter:

    arm throttle
    mode auto
    
De esta forma se armarán y realizarán la misión cargada anteriormente de forma automática. Estos son mensajes MAVLINK que desde la estación de tierra mandamos al dron simulado (contiene un Ardupilot que entiende MAVLINK) y finalmente, el dron realiza lo que le indiquemos.

Finalmente, con nuestra aplicación Android podremos conectarnos al simulador, recibir la información de telemetría y enviar los datos al servidor.

***

### Noticias interesantes: ###

Incidencias de drones con aviones en zonas restringidas:

* [Noticia 1](http://economia.elpais.com/economia/2016/03/02/actualidad/1456911759_020181.html)
* [Noticia 2](http://economia.elpais.com/economia/2016/03/04/actualidad/1457078339_462092.html)
* [Noticia 3](http://www.elmundo.es/internacional/2016/03/04/56d93e71e2704e3d4c8b45f6.html)

Los problemas con drones en las noticias anteriores, han ocurrido por la no disposición de suficientes aplicaciones que traten la seguridad para drones. Esta aplicación intentará solucionar dichos problemas.




