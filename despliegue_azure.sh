#!/bin/bash

#Se avisa si no se tiene permisos de administrador para que el usuarios los ponga

if [[ $EUID -ne 0 ]]; then
	echo "Debes tener permisos de administrador para ejecutar el script"

else
	# Variables

	APPENGINE_SERVER="GoogleAppEngineSDK/dev_appserver.py"

	#Iniciamos los módulos de GAE

	git submodule init && \
	git submodule sync && \
	git submodule update

	# Lanzar aplicación (con autoconfirmación)

	echo y | python $APPENGINE_SERVER  src --host=0.0.0.0 --port=80 --admin_port=8080 --storage_path=database &

fi
