#!/bin/bash

#Se avisa si no se tiene permisos de administrador para que el usuarios los ponga

if [[ $EUID -ne 0 ]]; then
	echo "Debes tener permisos de administrador para ejecutar el script"

else	
	mavproxy.py --master tcp:127.0.0.1:5760 --out 127.0.0.1:14550 &
fi
