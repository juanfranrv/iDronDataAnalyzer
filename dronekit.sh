#!/bin/bash

#Se avisa si no se tiene permisos de administrador para que el usuarios los ponga

if [[ $EUID -ne 0 ]]; then
	echo "Debes tener permisos de administrador para ejecutar el script"

else

	if [[ $(dpkg-query -W -f='${Status}\n' python) != 'install ok installed' ]]; then
		apt-get install -y --force-yes python
	fi
	
	if [[ $(dpkg-query -W -f='${Status}\n' python-pip) != 'install ok installed' ]]; then
		apt-get install -y --force-yes python-pip
	fi

	apt-get install python-dev

	pip install dronekit

	pip install dronekit-sitl

	pip install MAVProxy 

	dronekit-sitl copter &
fi
