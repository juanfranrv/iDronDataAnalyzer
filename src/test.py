import unittest
from google.appengine.ext import db
from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util
import urllib


class TestModel(db.Model):
  """A model class used for testing."""
  number = db.IntegerProperty(default=42)
  text = db.StringProperty()

class TestEntityGroupRoot(db.Model):
  """Entity group root"""
  pass

def GetEntityViaMemcache(entity_key):
  """Get entity from memcache if available, from datastore if not."""
  entity = memcache.get(entity_key)
  if entity is not None:
    return entity
  entity = TestModel.get(entity_key)
  if entity is not None:
    memcache.set(entity_key, entity)
  return entity

# Clase que comprueba que las urls son válidas y devuelven páginas html. En caso negativo no se pasa el test. 
   
class Tests(webapp2.RequestHandler):
    
    def get(self):
        self.response.write('TEST')

#Test inicial para probar si los test funcionan, usando el cuadrado de un número

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
              '/grafico', '/estadisticas', '/getDatosAtmosfericos', '/datos_grafico', '/pronostico', '/recibirDatosDrone', 
	      '/recibirDatosLoginApp', '/updateDatosDrone', '/METAR_TAF']
        
        for url in urls_test:
            response=urllib.urlopen('http://idrondataanalyzer.appspot.com' + url)
            if response.getcode() >= 400:
                return False
                
        return True


#Comprueba si la página web está activa

    def testPaginaActiva(self):

	response=urllib.urlopen('http://idrondataanalyzer.appspot.com')
	if response.getcode() >= 400:
	        return False
	return True


class iDronTestCase(unittest.TestCase):
	

	def setUp(self):
		# First, create an instance of the Testbed class.
		self.testbed = testbed.Testbed()
		# Then activate the testbed, which prepares the service stubs for use.
		self.testbed.activate()
		# Initialize the datastore stub with this policy.
		self.testbed.init_datastore_v3_stub()
		self.testbed.init_memcache_stub()

	def tearDown(self):
		self.testbed.deactivate()
		
	def test(self):
		pruebas = Tests()
		
		#Probamos el test inicial
		response = pruebas.testInicial(2)
		self.assertEqual(response,4)
		
		#Probamos que las url esten funcionando
		response = pruebas.testURL()
		self.assertEqual(response, True)
		
		#Probamos que la pagina este activa
		respuesta = pruebas.testPaginaActiva()
		self.assertEqual(respuesta, True)
		
	# Probamos a insertar en la base de datos
	def testInsertEntity(self):
		TestModel().put()
		response = 1
		self.assertEqual(response, len(TestModel.all().fetch(2)))
		

if __name__ == '__main__':
    unittest.main()
