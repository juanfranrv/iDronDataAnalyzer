#!/usr/bin/python
# -⁻- coding: UTF-8 -*-

import unittest, urllib, webapp2, subprocess, model
from google.appengine.ext import db
from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util
from google.appengine.ext import ndb

# Clase con cada uno de los tests 
class Tests(webapp2.RequestHandler):
    
    def get(self):
        self.response.write('TEST')

    #Test inicial para probar que los tests funcionan correctamente, usando el cuadrado de un número
    def testInicial(self, numero=0):
        return numero*numero

    #Test que comprueba si la aplicación web acepta n peticiones simultáneas (ping)
    def testMaxPeticiones(self):

        num = 10
        host = "ping -c1 idrondataanalyzer.appspot.com"

        for i in range(num):
            p = subprocess.Popen(host, shell=True, stderr=subprocess.PIPE)
    
        while True:
            out = p.stderr.read(1)
            
            if out == '' and p.poll()!= None:
                break
            if out != '':
                if p.poll() != 0:
                    return False
                else:
                    return True

    #Test que testea cada una de las url accesibles a través de la web, si alguna no funciona bien se devuelve false
    def testURL(self):  
        
        urls_test = [ '/', '/logout', '/editar_perfil', '/formRegistro', '/login', '/geolocalizacion', '/coordenadas',
              '/grafico', '/estadisticas', '/getDatosAtmosfericos', '/datos_grafico', '/pronostico', '/updateDatosDrone', '/METAR_TAF']
        
        for url in urls_test:
            response=urllib.urlopen('http://idrondataanalyzer.appspot.com' + url)
            if response.getcode() >= 400:
                return False
                
        return True

    #Comprueba si la página web está activa, false en caso de que esté caída.
    def testPaginaActiva(self):

	response=urllib.urlopen('http://idrondataanalyzer.appspot.com')
	if response.getcode() >= 400:
	        return False
	return True

    #Comprueba si se inserta correctamente en cada una de las tablas que forman la base de datos
    def testInsercionBD(self):

	#Inserción tabla datos recibidos del drone
        datosRecibidos = model.DatosRecibidos()

        datosRecibidos.idDatos = '1'
        datosRecibidos.latitud = '1'
        datosRecibidos.longitud = '1'
        datosRecibidos.altura = '1'
        datosRecibidos.velocidad = '1'
        
        datosRecibidos.put()

	#Inserción tabla datos de usuario
	datosUsuario = model.Usuario()

	datosUsuario.idUsuario = 'pepe'
	datosUsuario.usuario = 'pepe'
	datosUsuario.password = 'pepe'
	datosUsuario.nombre = 'pepe'
	datosUsuario.apellido = 'pepe'
	datosUsuario.correo = 'pepe'
	datosUsuario.telefono = 'pepe'

	datosUsuario.put()

	#Inserción tabla datos atmosféricos
	datosAtmosf = model.DatosAtmosfericos()

	datosAtmosf.idUsuario = 'pepe'
	datosAtmosf.date = '01-10-2016 21:40'
	datosAtmosf.fecha = '01-10-2016'
	datosAtmosf.dia = '01'
	datosAtmosf.mes = '10'
	datosAtmosf.anio = '2016'
	datosAtmosf.temperatura = 10.11
	datosAtmosf.pres_atmos = 10.11
	datosAtmosf.humedad = 10.11
	datosAtmosf.vel_viento = 10.11
	datosAtmosf.dir_viento = 10.11

	datosAtmosf.put()

	#Consultamos por id para comprobar si se han insertado en el test
        busquedaRec = model.DatosRecibidos.query(model.DatosRecibidos.idDatos == '1').get()
        busquedaAtmos = model.DatosAtmosfericos.query(model.DatosAtmosfericos.idUsuario == 'pepe').get()
        busquedaUser = model.Usuario.query(model.Usuario.idUsuario == 'pepe').get()

	if (busquedaRec or busquedaAtmos or busquedaUser) is None:
	        return False
	return True

    #Comprueba si se actualiza correctamente en cada una de las tablas que forman la base de datos
    def testActualizarBD(self):

	#Consultamos en la tabla de Datos recibidos los datos insertados en el test anterior y modificamos un campo
        busquedaRec = model.DatosRecibidos.query(model.DatosRecibidos.idDatos == '1').get()

        busquedaRec.idDatos = '10'
        busquedaRec.latitud = '1'
        busquedaRec.longitud = '1'
        busquedaRec.altura = '1'
        busquedaRec.velocidad = '1'

	busquedaRec.put()

	#Consultamos en la tabla de Datos atmosféricos insertados en el test anterior y modificamos un campo
        busquedaAtmos = model.DatosAtmosfericos.query(model.DatosAtmosfericos.idUsuario == 'pepe').get()

	busquedaAtmos.idUsuario = 'jacinto'
	busquedaAtmos.date = '01-10-2016 21:40'
	busquedaAtmos.fecha = '01-10-2016'
	busquedaAtmos.dia = '01'
	busquedaAtmos.mes = '10'
	busquedaAtmos.anio = '2016'
	busquedaAtmos.temperatura = 10.11
	busquedaAtmos.pres_atmos = 10.11
	busquedaAtmos.humedad = 10.11
	busquedaAtmos.vel_viento = 10.11
	busquedaAtmos.dir_viento = 10.11

	busquedaAtmos.put()

	#Consultamos en la tabla de Usuarios los datos insertados en el test anterior y modificamos un campo
        busquedaUser = model.Usuario.query(model.Usuario.idUsuario == 'pepe').get()

	busquedaUser.idUsuario = 'jacinto'
	busquedaUser.usuario = 'pepe'
	busquedaUser.password = 'pepe'
	busquedaUser.nombre = 'pepe'
	busquedaUser.apellido = 'pepe'
	busquedaUser.correo = 'pepe'
	busquedaUser.telefono = 'pepe'

	busquedaUser.put()

	#Consultamos posteriormente la base de datos para ver que efectivamente se han modificado correctamente
        busquedaRec = model.DatosRecibidos.query(model.DatosRecibidos.idDatos == '10').get()
        busquedaAtmos = model.DatosAtmosfericos.query(model.DatosAtmosfericos.idUsuario == 'jacinto').get()
        busquedaUser = model.Usuario.query(model.Usuario.idUsuario == 'jacinto').get()

	if (busquedaRec or busquedaAtmos or busquedaUser) is None:
	        return False
	return True

    #Comprueba si se borra correctamente en cada una de las tablas que forman la base de datos
    def testBorrarBD(self):

	#Borramos los datos insertados anteriormente 
        busquedaRec = model.DatosRecibidos.query(model.DatosRecibidos.idDatos == '10').get()
        busquedaAtmos = model.DatosAtmosfericos.query(model.DatosAtmosfericos.idUsuario == 'jacinto').get()
        busquedaUser = model.Usuario.query(model.Usuario.idUsuario == 'jacinto').get()

	busquedaRec.key.delete()
	busquedaAtmos.key.delete()
	busquedaUser.key.delete()

	#Si no existe devolvemos True ya que se han borrado
	if (busquedaRec or busquedaAtmos or busquedaUser) is None:
	        return True
	return False

#En esta clase vamos a ejecutar cada uno de los tests anteriores utilizando unittest.
class iDronTestCase(unittest.TestCase):

	def setUp(self):

		# Primero creamos una instace de testbed
		self.testbed = testbed.Testbed()
		# Después activamos testbed
		self.testbed.activate()
		# Inicializamos la datastore con esta política
		self.testbed.init_datastore_v3_stub()
		self.testbed.init_memcache_stub()

    		ndb.get_context().clear_cache()

	def tearDown(self):
		self.testbed.deactivate()
		
	def test(self):

		pruebas = Tests()
		
		#Probamos el test inicial
		response = pruebas.testInicial(2)
		self.assertEqual(response,4)
		
		#Probamos que las url estén funcionando
		response = pruebas.testURL()
		self.assertEqual(response, True)
		
		#Probamos que la pagina esté activa
		respuesta = pruebas.testPaginaActiva()
		self.assertEqual(respuesta, True)

		#Probamos que se inserten datos en la BD
		response = pruebas.testInsercionBD()
		self.assertEqual(respuesta, True)

		#Probamos que se actualizan datos en la BD
		response = pruebas.testActualizarBD()
		self.assertEqual(respuesta, True)

		#Probamos que se borran datos en la BD
		response = pruebas.testBorrarBD()
		self.assertEqual(respuesta, True)
				
#Lanzamos la batería de tests
if __name__ == '__main__':	

    unittest.main()

