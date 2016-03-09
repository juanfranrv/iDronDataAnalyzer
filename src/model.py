#!/usr/bin/python
# -⁻- coding: UTF-8 -*-

from google.appengine.ext import ndb

#Clase donde se define el modelo del usuario de la base de datos.

class Usuario(ndb.Model):
    usuario = ndb.StringProperty()
    password = ndb.StringProperty()
    nombre = ndb.StringProperty()
    apellido = ndb.StringProperty()
    correo = ndb.StringProperty()
    telefono = ndb.StringProperty()

#Clase donde se define el modelo de los datos atmosféricos monitorizados por el drone.

class DatosAtmosfericos(ndb.Model):
    fecha = ndb.StringProperty()
    temperatura = ndb.FloatProperty()
    pres_atmos = ndb.FloatProperty()
    humedad = ndb.FloatProperty()
    vel_viento = ndb.FloatProperty()
    dir_viento = ndb.FloatProperty()
