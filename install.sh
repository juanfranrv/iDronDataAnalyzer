#!/bin/bash

if [[ $EUID -ne 0 ]]; then
	echo "Debes tener permisos de administrador para ejecutar el script"

else

	echo 'Instalando aplicación...'

	if [ ! -d /usr/local/bin/iDronDataAnalyzer ]; then
		echo 'Copiando archivos en el sistema...'
		cp -r . /usr/local/bin/iDronDataAnalyzer
	fi

	sudo cp iDronDataAnalyzer /etc/init.d

	sudo update-rc.d iDronDataAnalyzer defaults
	sudo service iDronDataAnalyzer start

	echo '¡Listo!'

fi
