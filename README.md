# iDronDataAnalyzer (Seguridad para drones)

## Proyecto de fin de grado UGR && Talentum Telefónica ##

Actualmente está muy de moda el uso de drones para fines muy variados, desde misiones de reconocimiento hasta misiones de ataque. Cuando un drone está en movimiento, es conveniente tener una serie de personas encargadas de estudiar y observar los diversos datos que presenta la zona por la que va circulando, como la humedad, la temperatura, la velocidad del viento o la trayectoria, que son datos necesarios para decidir, por ejemplo, si cambiar la trayectoria del drone o ver si está en peligro. Para realizar estas tareas sería de gran utilidad la disposición de un sistema web que nos permita monitorizar y analizar dichos datos de suma importancia para el desarrollo con éxito de la misión.

Además, este sistema gestionará varios aspectos en el tema de "Seguridad en drones" que la mayoría de los usuarios desconoce, como es el acceso prohibido a aeropuertos, zonas de alta tensión, carreteras, edificios habitados... El drone detectará automáticamente estas zonas y obligará a que el usuario no pueda dirigirlo hacia ellas.

Se pretende desarrollar un sistema con un kit de utilidades destinadas a la realización de misiones con drones de forma eficaz, efectiva y segura. 

***

## Requisitos de la aplicación ##

La aplicación tendrá que cumplir los siguientes requisitos:

* [X] Monitorización y análisis de datos atmosféricos en tiempo real.  
* [ ] Seguimiento del drone utilizando el GPS incorporado.
* [X] Pronóstico de datos atmosféricos por horas o por días.
* [ ] Cálculo de estadísticos para el estudio general de la misión.
* [ ] Streaming en directo utilizando la cámara incorporada del dron.
* [X] Detección de los datos atmosféricos procedentes del METAR y TAF del aeropuerto más cercano por el que vaya circulando el drone en ese momento.
* [ ] Detección de zonas restringidas para el drone, prohibiendole el acceso.
* [ ] Incorporación de infraestructura virtual para automatizar varios aspectos del sistema: integración continua, entorno de pruebas, aprovisionamiento, instalación automática y despliegue automático.



