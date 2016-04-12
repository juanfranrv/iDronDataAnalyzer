FROM ubuntu:latest
MAINTAINER juanfranrv <juanfran0205rv@gmail.com>

#Instalar Python con todas las dependencias

RUN apt-get update
RUN apt-get -y install python python-setuptools build-essential python-dev
RUN apt-get install -y python-setuptools
RUN easy_install pip

# Instalar wget para descargar y zip para descomprimir

RUN apt-get install -y wget
RUN apt-get install -y zip

# Instalamos git y clonamos el repositorio
RUN apt-get install -y git
RUN git clone https://github.com/juanfranrv/iDronDataAnalyzer.git

# Descargamos los submódulos que faltan, GAE en este caso
# e iniciamos la instalación de la aplicación que incluye 
# el demonio de la misma

RUN cd iDronDataAnalyzer && \
git submodule init && \
git submodule sync && \
git submodule update && \
chmod 755 install.sh && \
bash install.sh

# Iniciamos el servicio
RUN service iDronDataAnalyzer restart



