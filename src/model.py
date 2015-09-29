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