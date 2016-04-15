#!/usr/bin/python
# -⁻- coding: UTF-8 -*-

import unittest, urllib, webapp2, subprocess
from google.appengine.ext import db
from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util

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
				
#Lanzamos la batería de tests
if __name__ == '__main__':	

    unittest.main()

