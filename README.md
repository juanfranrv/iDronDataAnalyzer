# iDronDataAnalyzer (Seguridad para drones)

## Proyecto de fin de grado UGR || Talentum Telefónica ##

Actualmente está muy de moda el uso de drones para fines muy variados, desde misiones de reconocimiento hasta misiones de ataque. Cuando un drone está en movimiento, es conveniente tener una serie de personas encargadas de estudiar y observar los diversos datos que presenta la zona por la que va circulando, como la humedad, la temperatura, la velocidad del viento o la trayectoria, que son datos necesarios para decidir, por ejemplo, si cambiar la trayectoria del drone o ver si está en peligro. Para realizar estas tareas sería de gran utilidad la disposición de un sistema web que nos permita monitorizar y analizar dichos datos de suma importancia para el desarrollo con éxito de la misión.

Además, este sistema gestionará varios aspectos en el tema de "Seguridad en drones" que la mayoría de los usuarios desconoce, como es el acceso prohibido a aeropuertos, zonas de alta tensión, carreteras, edificios habitados... El drone detectará automáticamente estas zonas y obligará a que el usuario no pueda dirigirlo hacia ellas.

Se pretende desarrollar un sistema con un kit de utilidades destinadas a la realización de misiones con drones de forma eficaz, efectiva y segura. 

***

## Requisitos de la aplicación ##

La aplicación tendrá que cumplir los siguientes requisitos:

* [X] Monitorización y análisis de datos atmosféricos en tiempo real.  
* [X] Seguimiento del drone utilizando el GPS incorporado. Además, se mostrarán los aeropuertos más cercanos (zona prohibida) y se podrá consultar la altura del terreno por el que va circulando el drone.
* [X] Pronóstico de datos atmosféricos por horas o por días.
* [ ] Cálculo de estadísticos para el estudio general de la misión.
* [ ] Streaming en directo utilizando la cámara incorporada del dron.
* [X] Detección de los datos atmosféricos procedentes del METAR y TAF del aeropuerto más cercano por el que vaya circulando el drone en ese momento.
* [ ] Detección de zonas restringidas para el drone, prohibiéndole el acceso. 
* [ ] Detección de vías aéreas más frecuentes.
* [ ] Incorporación de infraestructura virtual para automatizar varios aspectos del sistema: integración continua, entorno de pruebas, aprovisionamiento, instalación automática y despliegue automático.
 
***

## Requisitos: Conexión con drone ##

1. Con la aplicación web lanzada, las herramientas instaladas y el drone simulado junto con mavproxy (comunicación entre drone y aplicación) en el servidor (Azure), podemos comenzar a hacer pruebas y comprobar que los datos obtenidos son correctos.

2. El siguiente paso, sería probarlo con la IP del drone real y ver que sigue funcionando correctamente. Si esto ocurre, la aplicación funcionaría con datos reales aunque tenemos el problema del alcance y la distancia (zona wifi del drone limitada).

3. Una vez comprobado todo esto, pasaremos a estudiar dónde colocar mavproxy para que esté siempre al alcance de la zona wifi del drone.

4. Finalmente, ya tendremos todo funcionando con datos reales y una distancia prudente, por lo que pasaremos al desarrollo de las zonas restrictivas para el drone y a la comprobación del correcto funcionamiento de todas las herramientas implementadas utilizando datos reales extraídos de este.

***

## Para instalar la aplicación automáticamente: ##

Dar permisos y ejecutar el script [despliegue_azure.sh](https://github.com/juanfranrv/iDronDataAnalyzer/blob/master/despliegue_azure.sh). Inmediatamente, tendremos la aplicación lanzada en el puerto 8080.

***

## Para desplegar la aplicación en la nube automáticamente: ##

Dar permisos y ejecutar el script [despliegue_automatico_gae.sh](https://github.com/juanfranrv/iDronDataAnalyzer/blob/master/despliegue_automatico_gae.sh). Inmediatamente, tendremos la aplicación desplegada en la nube de Google App Engine.

***

## Para lanzar el simulador del drone: ##

1. Lanzar el script [dronekit.sh](https://github.com/juanfranrv/iDronDataAnalyzer/blob/master/dronekit.sh). Instalará las dependencias necesarias y lanzará un simulador de tipo drone.

2. Lanzar el script [mavproxy.sh](https://github.com/juanfranrv/iDronDataAnalyzer/blob/master/mavproxy.sh). De esta forma, tendremos el proxy activado para interpretar los mensajes MAVLINK que vamos a enviar al drone. Este proxy se conectará al drone simulado en el paso anterior.

3. Ejecutar el script de python [vehicle_state.py](https://github.com/juanfranrv/iDronDataAnalyzer/blob/master/src/iDronDataAnalyzer/vehicle_state.py) para comprobar que se muestran los datos deseados obtenidos del drone simulado.

***

## Noticias interesantes: ##

Choques de aviones con drones:

[Noticia 1](http://economia.elpais.com/economia/2016/03/02/actualidad/1456911759_020181.html)
[Noticia 2](http://economia.elpais.com/economia/2016/03/04/actualidad/1457078339_462092.html)
[Noticia 3](http://www.elmundo.es/internacional/2016/03/04/56d93e71e2704e3d4c8b45f6.html)

Los problemas con drones en las noticias anteriores, han ocurrido por la no disposición de suficientes aplicaciones que traten el tema de la seguridad para drones. Esta aplicación intentará arreglar dichos problemas.




