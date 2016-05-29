#!/usr/bin/python
# -⁻- coding: UTF-8 -*-

from google.appengine.ext import ndb

#Clase donde se define el modelo del usuario de la base de datos.

class Usuario(ndb.Model):
    idUsuario = ndb.StringProperty()
    usuario = ndb.StringProperty()
    tipo = ndb.StringProperty()
    password = ndb.StringProperty()
    nombre = ndb.StringProperty()
    apellido = ndb.StringProperty()
    correo = ndb.StringProperty()
    telefono = ndb.StringProperty()

#Clase donde se define el modelo de los datos atmosféricos monitorizados por el drone.

class DatosAtmosfericos(ndb.Model):
    idUsuario = ndb.StringProperty()
    date = ndb.StringProperty()
    latitud = ndb.StringProperty()
    longitud = ndb.StringProperty()
    ciudad = ndb.StringProperty()
    description = ndb.StringProperty()
    fecha = ndb.StringProperty()
    dia = ndb.StringProperty()
    mes = ndb.StringProperty()
    anio = ndb.StringProperty()
    temperatura = ndb.FloatProperty()
    max_temp = ndb.FloatProperty()
    min_temp = ndb.FloatProperty()
    pres_atmos = ndb.FloatProperty()
    humedad = ndb.FloatProperty()
    vel_viento = ndb.FloatProperty()
    dir_viento = ndb.FloatProperty()

#Clase donde se define el modelo de los datos recibidos en tiempo real desde el drone.

class DatosRecibidos(ndb.Model):
    idDatos = ndb.StringProperty()
    latitud = ndb.StringProperty()
    longitud = ndb.StringProperty()
    altura = ndb.StringProperty()
    velocidad = ndb.StringProperty()

