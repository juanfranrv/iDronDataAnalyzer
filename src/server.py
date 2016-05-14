#!/usr/bin/python
# -⁻- coding: UTF-8 -*-

from google.appengine.ext import ndb
from google.appengine.ext.webapp.util import run_wsgi_app
from collections import defaultdict
from google.appengine.api.urlfetch_errors import DeadlineExceededError
from google.appengine.api import urlfetch
import os, model, webapp2, jinja2, json, math, urllib, urllib2, sys, subprocess, random, datetime, time, uuid
from httplib import HTTPResponse
from google.appengine.api import urlfetch

# Declaración del entorno de jinja2 y el sistema de templates.

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#Cabecera y pie de pagina del html

head = JINJA_ENVIRONMENT.get_template('template/head.html').render()
footer = JINJA_ENVIRONMENT.get_template('template/footer.html').render()

#Variables globales

contador = 0                                    #Variable que lleva la cuenta para la inserción de datos en la base de datos

#Clase principal

class MainPage(webapp2.RequestHandler):
    
    def get(self):
        
        if self.request.cookies.get("username"):
            
            user=self.request.cookies.get("username")
            self.response.headers['Content-Type'] = 'text/html'
            template_values={'sesion':user,'footer': footer,'head':head}
            template = JINJA_ENVIRONMENT.get_template('template/index.html')
            self.response.write(template.render(template_values))
            
        else:
            
            self.redirect('/login')
            
#Clase para gestionar el inicio de sesión del usuario.

class Login(webapp2.RequestHandler):
    
    def get(self):
            
        self.response.headers['Content-Type'] = 'text/html'
        template_values={}
        template = JINJA_ENVIRONMENT.get_template('template/login.html')
        self.response.write(template.render(template_values))
    
    def post(self):
        
        usu=self.request.get('user')
        pas=self.request.get('pass')
        usur = None
        error = ''
        
        try:
            result=model.Usuario.query(model.Usuario.usuario==usu)
            usur=result.get()
        except:
            error = 'Error accessing the database: Required more quota than is available. Come back after 24h.'

        
        if usur is not None:

            if usur.password==pas:
                #Creamos una cookie para el nombre de usuario y otra para token
                self.response.headers.add_header('Set-Cookie',"username=" + str(usur.usuario))
                self.response.headers.add_header('Set-Cookie',"idUsername=" + str(usur.idUsuario))
                
                template_values={'sesion':usur.usuario,'head':head,'footer':footer}
                template = JINJA_ENVIRONMENT.get_template('template/index.html')
                self.response.write(template.render(template_values))
                                
                self.redirect('/')
                
            else:
        
                template_values={'mensaje':'Wrong password.'}
                template = JINJA_ENVIRONMENT.get_template('template/login.html')
                self.response.write(template.render(template_values))
        else:
            
            if error == '':   #Si no falla la quota, el error es por usuario incorrecto
                error = 'Wrong username.'
    
            template_values={'mensaje':error}
            template = JINJA_ENVIRONMENT.get_template('template/login.html')
            self.response.write(template.render(template_values))
            
# Clase que cierra la sesión del usuario.

class cerrar_sesion(webapp2.RequestHandler):
    
    def get(self):
        
        self.response.headers.add_header("Set-Cookie", "username=; Expires=Thu, 01-Jan-1970 00:00:00 GMT")
        self.redirect('/login')

#Clase que devuelve un formulario de registro.

class formRegistro(webapp2.RequestHandler):
    
    def get(self):
         
        self.response.headers['Content-Type'] = 'text/html'
        template_values={'message':"",'head':head}
        template = JINJA_ENVIRONMENT.get_template('template/registro.html')
        self.response.write(template.render(template_values))

    #Método que registra usuario si pasa las restricciones.

    def post(self):
        
        usuario_introducido = self.request.get('usuario')
        error = ''
        
        try:
            
            #Si el usuario no existe, se introducen los datos en la base de datos
            if model.Usuario.query(model.Usuario.usuario == usuario_introducido).get() is None:
                
                user = model.Usuario()
                datosRec = model.DatosRecibidos()
            
                token = str(uuid.uuid4())
                
                user.idUsuario = token
                user.usuario = self.request.get('usuario')
                user.password = self.request.get('password')
                user.nombre = self.request.get('nombre')
                user.apellido = self.request.get('apellido')
                user.correo = self.request.get('correo')
                user.telefono = self.request.get('telefono')
                            
                user.put()
                
                #Al registrarse el usuario inicializamos los datos recibidos del drone a 0, para que la aplicación no falle
                datosRec.idDatos = token
                datosRec.latitud = '37.187236'
                datosRec.longitud = '-3.779362' 
                datosRec.altura = '0.0'
                datosRec.velocidad = '0.0'
                
                datosRec.put()
                
                self.redirect('/')
                
            else:
                 #Si el usuario existe, se muestra un mensaje de error 
                error = 'Username is already in use'
            
        except:
             
            if error == '':   
                error = 'Error accessing the database: Required more quota than is available. Come back after 24h.'
                
        self.response.headers['Content-Type'] = 'text/html'
        template_values={'message':error}
        template = JINJA_ENVIRONMENT.get_template('template/registro.html')
        self.response.write(template.render(template_values))
 
#Clase para cambiar los datos de usuario

class editar_perfil(webapp2.RequestHandler):
    
    def get(self):
        
        if self.request.cookies.get("username"):  #Si la cookie está activada
            
            username = str(self.request.cookies.get("username"))
            usuarios = []
            error = ''
            
            try:
                result= model.Usuario.query(model.Usuario.usuario == username)
                
                if result is not None:    #Existe el usuario
                    
                    for usuario in result:  #Lo buscamos y lo añadimos al array de usuarios   
                        usuarios.append(usuario)
                        
            except:
                error = 'Error accessing the database: Required more quota than is available. Come back after 24h.'
                
                    
            self.response.headers['Content-Type'] = 'text/html'
            template_values = {'usuarios':usuarios, 'error':error, 'sesion':username, 'footer': footer,'head':head}
            template = JINJA_ENVIRONMENT.get_template('template/editar_perfil.html')
            self.response.write(template.render(template_values,message=""))
            
        else:
            
            self.redirect('/login')
            
    def post(self):
        
        if self.request.cookies.get("username"):
            
            username = str(self.request.cookies.get("username"))
            result = model.Usuario.query()
            
            for us in result:
                
                if us.usuario == username:            # Se introducen los nuevos datos modificados en la base de datos
                    
                    password = self.request.get('password')
                    name = self.request.get('nombre')
                    lastname = self.request.get('apellido')
                    email = self.request.get('correo')
                    phone = self.request.get('telefono')
                       
                    if password != "": us.password = password   #Si no se modifica algun dato, es decir, esta vacio, se deja el dato anterior
                    if name != "": us.nombre = name
                    if lastname != "": us.apellido = lastname
                    if email != "": us.correo = email
                    if phone != "": us.telefono = phone
                         
                    us.put()
                    self.redirect('/')
                    
#Clase que gestiona las url erróneas
             
class ErrorPage(webapp2.RequestHandler):
    
    def get(self):
        
        if self.request.cookies.get("username"):

            username = str(self.request.cookies.get("username"))
            self.response.headers['Content-Type'] = 'text/html'
            template_values={'sesion':username,'footer': footer,'head':head}
            template = JINJA_ENVIRONMENT.get_template('template/error.html')
            self.response.write(template.render(template_values))
            
        else:
            
            self.redirect('/login')

#Clase que recibe los datos  de login procedentes del HTTP POST de la aplicación de Android para devolver el token del usuario correspondiente

class RecibirDatosLoginApp(webapp2.RequestHandler):
    
    def post(self):
                
            username = self.request.get('username')
            password = self.request.get('password')
            token = "NoData"
            
            #Buscamos el usuario recibido desde Android en la base de datos y si existe devolvemos su token para iniciar sesión en la app Android
            UserQuery = model.Usuario.query(model.Usuario.usuario == username).get()
            
            if UserQuery is not None:
                
                if UserQuery.password == password:
                    token = UserQuery.idUsuario
                    self.response.write(token)
                    
                else:
                    self.response.write(token)
                
            else:    
                self.response.write(token)         
         
#Clase que recibe los datos procedentes del HTTP POST de la aplicación de Android y los almacena para ser tratados posteriormente en el resto de funcionalidades

class RecibirDatosDrone(webapp2.RequestHandler):
    
    def post(self):

            #Obtiene los datos recibidos por Http Post desde el drone (A través de la app de Android)
            token = self.request.get('token')
            latitud = self.request.get('latitud')
            longitud = self.request.get('longitud')
            altura = self.request.get('altura')
            velocidad = self.request.get('velocidad')
            
            busqueda = model.DatosRecibidos.query(model.DatosRecibidos.idDatos == token).get()
            
            if busqueda is None:    #Si la base de datos está vacía, insertamos los datos recibidos del drone
                
                datosRec = model.DatosRecibidos()
                        
                datosRec.idDatos = token
                datosRec.latitud = latitud
                datosRec.longitud = longitud
                datosRec.altura = altura
                datosRec.velocidad = velocidad
                
                datosRec.put()
            
            else:                   #Si ya no está vacía, buscamos los únicos datos que tiene y sobreescribimos por los nuevos
                
                busqueda.idDatos = token
                busqueda.latitud = latitud
                busqueda.longitud = longitud
                busqueda.altura = altura
                busqueda.velocidad = velocidad
                
                busqueda.put()
                  
#Clase que gestiona el googlemap de geolocalización
             
class geolocalizacion(webapp2.RequestHandler):
    
    def get(self):
        
        if self.request.cookies.get("username"):
            
            #Inicialización de variables
            lat = 37.187236
            lng = -3.779362
            vel = 0
            alt = 0
            error = ''
            
            try:
                
                username = str(self.request.cookies.get("username"))
                idUsername = self.request.cookies.get("idUsername")
     
                datos = model.DatosRecibidos.query(model.DatosRecibidos.idDatos == idUsername).get()
            
                lat = datos.latitud
                lng = datos.longitud
    
                vel = round(float(datos.velocidad),3)
                alt = round(float(datos.altura),3)
            
            except:
                error = 'Error accessing the database: Required more quota than is available. Come back after 24h.'
    
            try:
                
                url = 'http://api.sunrise-sunset.org/json?lat=' + str(lat) + '&lng=' + str(lng)
                
                r = urllib2.urlopen(url)
            
                sunset_sunrise = json.load(r)
            
            except (ValueError, KeyError, DeadlineExceededError) as e:
                
                if error == '':
                    error = "Sunset and sunrise is temporarily unavailable"
                    
            self.response.headers['Content-Type'] = 'text/html'
            template_values={'sesion':username, 'sunset_sunrise':sunset_sunrise, 'error':error, 'footer': footer,'head':head,'lat':lat,'lng':lng,'vel':vel,'alt':alt}
            template = JINJA_ENVIRONMENT.get_template('template/geolocalizacion.html')
            self.response.write(template.render(template_values))
                        
        else:
            
            self.redirect('/login')

# Clase que genera las coordenadas del dron.

class coordenadas(webapp2.RequestHandler):
    
    def get(self):
        
        if self.request.cookies.get("username"):
 
            alert = 0
            datosRec = []
            idUsername = self.request.cookies.get("idUsername")
            
            coordenadas = model.DatosRecibidos.query(model.DatosRecibidos.idDatos == idUsername).get()
            
            lat = coordenadas.latitud
            lng = coordenadas.longitud
            
            vel = round(float(coordenadas.velocidad),3)
            alt = round(float(coordenadas.altura),3)
            
            if alt > 120:       #Si la altura es mayor de 120m, lanzamos alerta ya que está prohibido
                alert = 1
      
            datosRec.append({'latitud': lat,
                             'longitud': lng,
                             'velocidad': vel,
                             'altura': alt,
                             'alert':alert
                           })
                
            self.response.write(json.dumps(datosRec))

#Clase que obtiene las ciudades cercanas a una zona

class getNearbyAreas(webapp2.RequestHandler):
    
    def get(self):
        
        if self.request.cookies.get("username"):
            
            try:  

                #Hacemos petición al servicio web de geonames y mandamos el json al template
                idUsername = self.request.cookies.get("idUsername")
            
                coordenadas = model.DatosRecibidos.query(model.DatosRecibidos.idDatos == idUsername).get()
                
                lat = coordenadas.latitud
                lng = coordenadas.longitud

                #Deadline error http, poner default fetch
                urlfetch.set_default_fetch_deadline(45)
                
                url = 'http://api.geonames.org/findNearbyJSON?username=juanfranrv&country=US&lat=' + str(lat) + '&lng=' + str(lng) + '&radius=300&formatted=true&featureCode=PPL&featureClass=P'
                
                r = urllib2.urlopen(url)
        
                result = json.load(r)
                populationAreas = []
                               
                populationAreas = result["geonames"]
 
                self.response.write(json.dumps(populationAreas))
                
            except (ValueError, KeyError, DeadlineExceededError) as e:
                
                error = 'Geonames web service is temporarily unavailable.'
                self.response.write(json.dumps(error))
        
#Clase que obtiene el tráfico aéreo en tiempo real

class getNearbyFlights(webapp2.RequestHandler):
    
    def get(self):
        
        if self.request.cookies.get("username"):
            #Hacemos petición al servicio web de flightstats y mandamos el json al template        
            try:
                
                idUsername = self.request.cookies.get("idUsername")
                
                coordenadas = model.DatosRecibidos.query(model.DatosRecibidos.idDatos == idUsername).get()
            
                lat = coordenadas.latitud
                lng = coordenadas.longitud
                
                url = "https://api.flightstats.com/flex/flightstatus/rest/v2/json/flightsNear/" + str(lat) + "/" + str(lng) +"/50?appId=3f8a0b42&appKey=bf48b6de9b12bbb5ccb59c09834c4302&maxFlights=10"
                
                r = urllib2.urlopen(url)
        
                result = json.load(r)
                flights= []
                
                for i in range(len(result["flightPositions"])):
                    last_flight_detected = result["flightPositions"][i]["positions"][len(result["flightPositions"][i]["positions"])-1]
                    flights.append(last_flight_detected)
                
                self.response.write(json.dumps(flights))
                
            except (ValueError, KeyError, DeadlineExceededError) as e:
                
                error = 'Flightstats web service is temporarily unavailable.'
                self.response.write(json.dumps(error))
                         
#Clase que gestiona el gráfico de monitorización de datos atmosféricos en tiempo real
             
class grafico(webapp2.RequestHandler):
    
    def get(self):
        
        if self.request.cookies.get("username"):
            
            username = str(self.request.cookies.get("username"))
            
            self.response.headers['Content-Type'] = 'text/html'
            template_values={'sesion':username,'footer': footer,'head':head}
            template = JINJA_ENVIRONMENT.get_template('template/grafico.html')
            self.response.write(template.render(template_values))
            
        else:
            
            self.redirect('/login') 
            
# Clase que genera datos aleatorios provisionales para el gráfico

class datos_grafico(webapp2.RequestHandler):
    
    def get(self):
        
        if self.request.cookies.get("username"):
                
            try:
                global contador
                datoAmostrar = ''
                Api_key = 'fffa0ba60d5357235f5782313216b8ae'    #Key para la API del gráfico de monitorización
                idUsername = self.request.cookies.get("idUsername")               
               
                coordenadas = model.DatosRecibidos.query(model.DatosRecibidos.idDatos == idUsername).get()
                
                lat = coordenadas.latitud
                lng = coordenadas.longitud
                
                url = 'http://api.openweathermap.org/data/2.5/weather?lat=' + str(lat) + '&lon=' + str(lng) + '&appid=' + Api_key
                r = urllib2.urlopen(url)
        
                result = json.load(r)
                
                tempe = result["main"]["temp"]          #temperatura
                pres = result["main"]["pressure"]       #presion atmosferica
                hum = result["main"]["humidity"]        #humedad
                vel_wind = result["wind"]["speed"]      #velocidad del viento
                dir_win = result["wind"]["deg"]         #direccion del viento
                
                temp = tempe - 273.15                   #conversión de kelvin a celsius
                vel_win = vel_wind * 3.6                #conversión de m/s a km/h
        
                dato_seleccionado = self.request.get('dato')
        
                if dato_seleccionado == 'undefined' or dato_seleccionado == 'Temperature':
                    datoAmostrar = temp;
                elif dato_seleccionado == 'Atmospheric pressure':
                    datoAmostrar = pres;
                elif dato_seleccionado == 'Humidity':
                    datoAmostrar = hum;
                elif dato_seleccionado == 'Wind Speed':
                    datoAmostrar = vel_win;
                elif dato_seleccionado == 'Wind Direction':
                    datoAmostrar = dir_win;
                
                if contador is 80:         #Cada 80 datos obtenidos, almacenamos en la base de datos
                    #Almacenamos los datos en el usuario con la sesión activa
                    data = model.DatosAtmosfericos()
                    
                    data.fecha = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
                    data.date = datetime.datetime.now().strftime("%d-%m-%Y")
                    data.idUsuario = idUsername
                    data.dia = datetime.date.today().strftime("%V")        #Obtiene el número de la semana 
                    data.mes = datetime.date.today().strftime("%m")
                    data.anio = datetime.date.today().strftime("%Y")  
                    data.temperatura = round(temp,2)
                    data.pres_atmos = round(pres,2)
                    data.humedad = hum
                    data.vel_viento = round(vel_win,2)
                    data.dir_viento = round(dir_win,2)
                    
                    data.put()
                    
                    contador = 0
                
                else:
                    contador = contador + 1
                
                self.response.write(json.dumps(datoAmostrar)) 
                
            except (ValueError, KeyError, DeadlineExceededError) as e:
                
                error = 'Chart web service is temporarily unavailable.'
                self.response.write(json.dumps(error))

#Clase para borrar datos procedentes de estadisticas

class deleteStatistic(webapp2.RequestHandler):
    
    def get(self):
        
        deleteID = long(self.request.get("id"))

        weatherData = model.DatosAtmosfericos.get_by_id(deleteID)   #Elimina el dato elegido por el usuario
        weatherData.key.delete()
        
        self.response.write(json.dumps("Deleted")) 
                 
#Clase que gestiona las estadisticas de la monitorización de datos atmosféricos obtenida

class estadisticas(webapp2.RequestHandler):
    
    def get(self):
                
        if self.request.cookies.get("username"):
    
            username = str(self.request.cookies.get("username"))
                        
            self.response.headers['Content-Type'] = 'text/html'
            template_values={'sesion':username,'footer': footer,'head':head}
            template = JINJA_ENVIRONMENT.get_template('template/estadisticas.html')
            self.response.write(template.render(template_values))
            
        else:
            
            self.redirect('/login') 
            
#Clase que devuelve los datos atmosféricos almacenados en la base de datos

class getDatosAtmosfericos(webapp2.RequestHandler):
    
    def get(self):
        
        if self.request.cookies.get("username"):
            
            datos_atmos = []
            fecha_elegida = self.request.get('fecha') 
            tiempo_elegido = self.request.get('tiempo')
            idUsername = self.request.cookies.get("idUsername")
                        
            if tiempo_elegido == 'mensual':     #Si el tiempo es mensual, comprobamos el mes antes de añadir
                result = model.DatosAtmosfericos.query(model.DatosAtmosfericos.mes == fecha_elegida[3:5], model.DatosAtmosfericos.anio == fecha_elegida[6:11], model.DatosAtmosfericos.idUsuario == idUsername).order(model.DatosAtmosfericos.fecha)
            
            elif tiempo_elegido == 'semanal':
                num_semana = datetime.date(int(fecha_elegida[6:11]), int(fecha_elegida[3:5]), int(fecha_elegida[0:2])).strftime("%V") 
                result = model.DatosAtmosfericos.query(model.DatosAtmosfericos.dia == num_semana, model.DatosAtmosfericos.anio == fecha_elegida[6:11], model.DatosAtmosfericos.idUsuario == idUsername).order(model.DatosAtmosfericos.fecha)
                                                
            elif tiempo_elegido == 'anual':     #Si el tiempo es anual, comprobamos el año antes de añadir
                result = model.DatosAtmosfericos.query(model.DatosAtmosfericos.anio == fecha_elegida[6:11], model.DatosAtmosfericos.idUsuario == idUsername).order(model.DatosAtmosfericos.fecha).order(model.DatosAtmosfericos.mes)

            else:          
                result = model.DatosAtmosfericos.query(model.DatosAtmosfericos.date  == fecha_elegida, model.DatosAtmosfericos.idUsuario == idUsername).order(model.DatosAtmosfericos.fecha)

            if result is not None: 
                         
                for dato in result:             #Crear un array de tipo json para parsear en el cliente    
                         datos_atmos.append({'fecha': dato.fecha,
                                            'temperatura': dato.temperatura,
                                            'presion': dato.pres_atmos,
                                            'humedad': dato.humedad,
                                            'vel_viento': dato.vel_viento,
                                            'dir_viento': dato.dir_viento,
                                            'id': dato.key.id()
                                            })

            self.response.write(json.dumps(datos_atmos)) 
                        
        else:
            
            self.redirect('/login') 
                       
#Clase que gestiona el pronóstico de datos atmosféricos en tiempo real
             
class pronostico(webapp2.RequestHandler):
    
    def get(self):
        
        if self.request.cookies.get("username"):
            
            username = str(self.request.cookies.get("username"))
            
            self.response.headers['Content-Type'] = 'text/html'
            template_values={'sesion':username,'footer': footer,'head':head}
            template = JINJA_ENVIRONMENT.get_template('template/pronostico.html')
            self.response.write(template.render(template_values))
            
        else:
            
            self.redirect('/login')   
            
    def post(self):
        
        if self.request.cookies.get("username"):

            username = str(self.request.cookies.get("username"))
            
            latitud = self.request.get('latitud')
            longitud = self.request.get('longitud')
            radio_elegido = self.request.get('optradio')
            
            API_pronostico = 'c6f8c98fd1da5785'             #Key para la API del pronóstico
            array_datos = []
            error = ''
            latitud_actual = ''
            longitud_actual = ''
            
            try:
                
                if radio_elegido == 'horas':
                    
                    url_horas = 'http://api.wunderground.com/api/' + API_pronostico + '/hourly/conditions/lang:EN/q/' + str(latitud) + ',' + str(longitud) + '.json'
                    
                    r = urllib2.urlopen(url_horas)
                    result = json.load(r)
                        
                    for i in range(36):                                
                        array_datos.append(result["hourly_forecast"][i])
                                         
                else: 
                    
                    url_dias = 'http://api.wunderground.com/api/' + API_pronostico + '/forecast10day/conditions/lang:EN/q/' + str(latitud) + ',' + str(longitud) + '.json'
    
                    r = urllib2.urlopen(url_dias)
                    result = json.load(r)
                    
                    for i in range(10):                          
                        array_datos.append(result["forecast"]["simpleforecast"]["forecastday"][i])
                
                latitud_actual = result["current_observation"]["display_location"]["latitude"]
                longitud_actual = result["current_observation"]["display_location"]["longitude"]
                
            except (ValueError, KeyError, DeadlineExceededError) as e:
                error = 'There is not any city with those coordinates. Please, verify the place.'
                
            self.response.headers['Content-Type'] = 'text/html'
            template_values={'sesion':username, 
                             'array_datos':array_datos,
                             'radio_elegido':radio_elegido,
                             'latitud_actual':latitud_actual,
                             'longitud_actual':longitud_actual,
                             'error':error,
                             'head':head,
                             'footer':footer
                             }
            
            template = JINJA_ENVIRONMENT.get_template('template/pronostico.html')
            self.response.write(template.render(template_values))
            
        else:
            
            self.redirect('/login')
       
#Obtiene la descripción de cada nubosidad para el METAR y TAF parseando el resultado

def getInfoNubosidad(nube, altura): 
    
    str_altura = list(altura)   #Pasamos a lista para borrar los 0, y luego volvemos a convertir a string
    
    if altura[:1] == '0':
        str_altura.remove('0')
        if altura[:2] == '00':
            str_altura.remove('0')

    altura = ''.join(str_altura)
    result = ''
    
    if nube == 'SKC':
        result = 'SKC - Clear sky at ' + altura + '00 pies. Clean sky below 12.000 for ASOS/AWOS.'
    elif nube == 'FEW':
        result = 'FEW - Few clouds at ' + altura + '00 feet. Clouds cover between  1/8 and 2/8 of sky.'
    elif nube == 'SCT':   
        result = 'SCT - Scattered clouds at ' + altura + '00 feet. Clouds cover between 3/8 and 4/8 of sky.' 
    elif nube == 'BKN': 
        result = 'BKN - Broken clouds at ' + altura + '00 feet. Clouds cover between 5/8 and 7/8 of sky.'  
    elif nube == 'OVC':
        result = 'OVC - Covered sky at ' + altura + '00 feet (overcast).'    
    elif nube == 'TCU': 
        result = 'TCU - Towering cumulus at ' + altura + '00 feet.'  
    elif nube == 'CB':
        result = 'CB - Cumulonimbus at ' + altura + '00 feet. Cumulonimbus are dense vertical formations that can cause heavy rainfall , thunderstorms or hail' 
    elif nube == 'CAVOK': 
        result = 'CAVOK - Visibility is perfect at ' + altura + '00 feet (Conditions are perfect for flying)'
    else:   
        result = 'empty'

    return result

#Parsea la información obtenida y devuelve un JSON con el METAR legible

def parseoMETAR(result_metar):
    
    #Inicialización de variables
    array_nubes = []
    metar = ''
    temperatura = ''
    presion_atmosferica = ''
    nubes = ''
    fecha_captura = ''
    visibilidad = ''
    direccion_viento = ''
    velocidad_viento = ''
    rafaga_viento = ''

    #Inicio del parseo
    metar = result_metar["Raw-Report"]
    temperatura = result_metar["Temperature"] + ' C'
    presion_atmosferica = result_metar["Altimeter"] + ' hPa'
    nubes = result_metar["Cloud-List"]
     
    for nube in nubes:                          #Recorremos el array de nubes obtenidas
        array_nubes.append(getInfoNubosidad(nube[0], nube[1]))

    fecha_captura = result_metar["Time"]        #Parseo para obtener del string el dia y hora
    dia = fecha_captura[:2]
    hora = fecha_captura[2:4] + ':' + fecha_captura[4:6] + ' UTC'
     
    visibilidad = result_metar["Visibility"] + ' m'
    if visibilidad == '9999 m':                #Si la visibilidad es 9999 significa que hay 10km o mas
        visibilidad = '10km or more'
         
    direccion_viento = result_metar["Wind-Direction"] + ' degrees'
    if direccion_viento == '000 degrees':       #No hay viento
        direccion_viento = 'No wind'
    elif direccion_viento == "VRB degrees":
        direccion_viento = 'Wind in all directions '
         
    rafaga_viento = result_metar["Wind-Gust"] + ' KT'
     
    velocidad_viento = result_metar["Wind-Speed"] + ' KT'
    if velocidad_viento == '00 KT':                #No hay viento
        velocidad_viento = 'There is not wind'
     
    if len(array_nubes) is 0:
        array_nubes.append('No data')
    if rafaga_viento == ' KT':
        rafaga_viento = 'No data'
    if temperatura == ' C':
        temperatura = 'No data'
    if visibilidad == ' m':
        visibilidad = 'No data'
    if direccion_viento == ' degrees':
        direccion_viento = 'No data'
    if velocidad_viento == ' KT':
        rafaga_viento = 'No data'
     
    #Devolución de JSON con los datos parseados      
    datos_metar =  {'presion_atmosferica':presion_atmosferica,
                    'visibilidad':visibilidad,
                    'direccion_viento':direccion_viento,
                    'rafaga_viento':rafaga_viento,
                    'velocidad_viento':velocidad_viento,
                    'temperatura':temperatura,
                    'metar':metar,
                    'array_nubes':array_nubes,
                    'dia':dia,
                    'hora':hora,
                    }
    
    return datos_metar

#Parsea la información obtenida (no repetida) y devuelve un JSON con el TAFOR legible

def parseoTAFOR_noRepeatInfo(result_taf):

    #Inicialización de variables
    array_nubes_taf = defaultdict(list)
    taf = ''
    max_temp = ''
    min_temp = ''
  
    taf = result_taf["Raw-Report"]
    
    fecha_captura_taf = result_taf["Time"]        #Parseo para obtener del string el dia y hora
    dia_taf = fecha_captura_taf[:2]
    hora_taf = fecha_captura_taf[2:4] + ':' + fecha_captura_taf[4:6]
    
    max_temp = result_taf["Max-Temp"]
    min_temp = result_taf["Min-Temp"]

    if max_temp == '':
        max_temp = "No data"
    else:
        max_temp = max_temp[2:4] + " C"
      
    if min_temp == '':
        min_temp = "No data"
    else:
        min_temp = min_temp[2:4] + " C"
        
    for i in range(len(result_taf["Forecast"])):

        if result_taf["Forecast"][i]["Cloud-List"] == []:
            array_nubes_taf[i].append('No data')
            
        else:
            
            for nube in result_taf["Forecast"][i]["Cloud-List"]:    #Recorremos el array de nubes obtenidas
                array_nubes_taf[i].append(getInfoNubosidad(nube[0], nube[1]))
         
    #Devolución de JSON con los datos parseados  
    datos_taf = {'taf':taf,
                'max_temp':max_temp,
                'min_temp':min_temp,
                'dia_taf':dia_taf,
                'hora_taf':hora_taf,
                'array_nubes_taf':array_nubes_taf
                }

    return datos_taf

#Parsea la información obtenida (repetida, tal como todos los datos atmosféricos pronosticados) y devuelve un JSON con el TAFOR legible

def parseoTAFOR_RepeatInfo(result_taf):

    #Inicialización de variables  
    datos_tafN = []
    array_taf = []
    presion = ''
    visibilidad = ''
    dir_viento = ''
    vel_viento = ''
    rafaga_viento = ''
    
    for i in range(len(result_taf["Forecast"])):    #Rellenamos el array con la info obtenida de la API
        array_taf.append(result_taf["Forecast"][i])
        
    for taf in array_taf:                           #Parseamos la información y la guardamos en un dict
        
        if taf["Altimeter"] == '':
            presion = 'No data'
        else:
            presion = taf["Altimeter"] + ' hPa'
            
        if taf["Visibility"] == '9999':
            visibilidad = '10km or more'
        elif taf["Visibility"] == '':
            visibilidad = 'No data'
        else:
            visibilidad = taf["Visibility"] + ' m'
            
        if taf["Wind-Direction"] == '':
            dir_viento = 'No data'
        elif taf["Wind-Direction"] == 'VRB':
            dir_viento = 'Wind in all directions'
        elif taf["Wind-Direction"] == '000 degrees':
            dir_viento = 'No wind'
        else:
            dir_viento = taf["Wind-Direction"] + ' degrees'
            
        if taf["Wind-Gust"] == '':
            rafaga_viento = 'No data'
        else:
            rafaga_viento = taf["Wind-Gust"] + ' KT'
            
        if taf["Wind-Speed"] == '':
            vel_viento = "No data"
        else:
            vel_viento = taf["Wind-Speed"] + ' KT'

        #Devolución de JSON con los datos parseados  
        datos_tafN.append({'presion':presion,
                          'vel_viento':vel_viento,
                          'rafaga_viento':rafaga_viento,
                          'dir_viento':dir_viento,
                          'visibilidad':visibilidad,
                          'dia':taf["Start-Time"][:2],
                          'hora':taf["Start-Time"][2:4],
                          'dia_fin':taf["End-Time"][:2],
                          'hora_fin':taf["End-Time"][2:4],
                        })

    return datos_tafN
    
# Clase que genera los datos atmosféricos obtenidos de aeropuertos como son el TAF y METAR

class METAR_TAF(webapp2.RequestHandler):
    
    def get(self):
        
        if self.request.cookies.get("username"):

            #Inicialización de variables para que siga funcionando en el que caso de que no exista alguna
                 
            lat = ''                   
            lng = ''
            error = ''
            username = str(self.request.cookies.get("username")) 
            array_metar = []
            array_taf = []
            array_tafN = []
            idUsername = self.request.cookies.get("idUsername")
            
            try:    #Comprobacion error de quota
                       
                coordenadas = model.DatosRecibidos.query(model.DatosRecibidos.idDatos == idUsername).get()
                
                lat = coordenadas.latitud
                lng = coordenadas.longitud
                
            except:
                
                error = 'Error accessing the database: Required more quota than is available. Come back after 24h.'

            #Gestión del METAR y parseo de la información para su interpretación
                 
            try:
                
                #Deadline error http, poner default fetch
                urlfetch.set_default_fetch_deadline(45)
                
                url_metar = 'http://avwx.rest/api/metar.php?lat=' + str(lat) + '&lon=' + str(lng) + '&format=JSON'
            
                r_metar = urllib2.urlopen(url_metar)
                result_metar = json.load(r_metar)
                                    
                array_metar = parseoMETAR(result_metar)             #Llamamos a la función parseadora
                
                #Gestión del TAF y parseo de alguna de la información para su interpretación. La otra parte esta en el template interpretada
                 
                url_taf = 'http://avwx.rest/api/taf.php?lat=' + str(lat) + '&lon=' + str(lng) + '&format=JSON'
                                                           
                r_taf = urllib2.urlopen(url_taf)
                result_taf = json.load(r_taf)

                array_tafN = parseoTAFOR_noRepeatInfo(result_taf)   #Llamamos a las funciones parseadoras
                array_taf = parseoTAFOR_RepeatInfo(result_taf)
                
            except (ValueError, KeyError, DeadlineExceededError) as e:
                #No se pueden dar dos errores a la vez
                if error == '':    #Si el error de quota está activo se mantiene, si es nulo se modifica
                    error = 'TAFOR or METAR  is temporarily unavailable.'
                
            self.response.headers['Content-Type'] = 'text/html'

            template_values={'sesion':username,
                             'array_metar':array_metar,
                             'array_taf':array_taf,
                             'array_tafN':array_tafN,
                             'error':error, 
                             'footer': footer,
                             'head':head
                            }
            
            template = JINJA_ENVIRONMENT.get_template('template/pronostico_aeropuertos.html')
            self.response.write(template.render(template_values)) 
            
        else:
            
            self.redirect('/login')
              
# Urls de la aplicación con sus clases asociadas.

urls = [('/', MainPage),
        ('/login', Login),
        ('/formRegistro',formRegistro),
        ('/logout', cerrar_sesion),
        ('/editar_perfil', editar_perfil),
        ('/geolocalizacion', geolocalizacion),
        ('/coordenadas', coordenadas),
        ('/grafico', grafico),
        ('/estadisticas', estadisticas),
        ('/getDatosAtmosfericos', getDatosAtmosfericos),
        ('/datos_grafico', datos_grafico),
        ('/pronostico', pronostico),
        ('/recibirDatosDrone', RecibirDatosDrone),
        ('/recibirDatosLoginApp',RecibirDatosLoginApp),
        ('/METAR_TAF', METAR_TAF),
        ('/getNearbyAreas', getNearbyAreas),
        ('/getNearbyFlights', getNearbyFlights),
        ('/deleteStatistic', deleteStatistic),
        ('/.*', ErrorPage)
       ]

# Creamos la aplicación asignando al URL Dispacher las urls previamente definidas.

application = webapp2.WSGIApplication(urls, debug=True)
    
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
