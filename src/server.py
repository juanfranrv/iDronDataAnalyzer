#!/usr/bin/python
# -⁻- coding: UTF-8 -*-

from google.appengine.ext import ndb
from google.appengine.ext.webapp.util import run_wsgi_app
from collections import defaultdict
from google.appengine.runtime import DeadlineExceededError
from google.appengine.api import urlfetch
import os
import model
import webapp2
import jinja2
import json
import math
import urllib
import urllib2
import sys
import subprocess
import random

# Declaración del entorno de jinja2 y el sistema de templates.

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#Clase principal

class MainPage(webapp2.RequestHandler):
    
    def get(self):
        
        if self.request.cookies.get("username"):
            
            user=self.request.cookies.get("username")
            self.response.headers['Content-Type'] = 'text/html'
            template_values={'sesion':user}
            template = JINJA_ENVIRONMENT.get_template('template/index.html')
            self.response.write(template.render(template_values))
            
        else:
            
            self.response.headers['Content-Type'] = 'text/html'
            template_values={}
            template = JINJA_ENVIRONMENT.get_template('template/login.html')
            self.response.write(template.render(template_values))
            
#Clase para gestionar el inicio de sesión del usuario.

class Login(webapp2.RequestHandler):
    
    def get(self):
            
            self.response.headers['Content-Type'] = 'text/html'
            template_values={}
            template = JINJA_ENVIRONMENT.get_template('template/login.html')
            self.response.write(template.render(template_values))
    
    def post(self):
        
        usu=self.request.get('user')
        result=model.Usuario.query(model.Usuario.usuario==usu)
        usur=result.get()
        
        if usur is not None:
            
            usur=result.get()
            pas=self.request.get('pass')
            
            if usur.password==pas:
                
                self.response.headers.add_header('Set-Cookie',"username="+str(usur.usuario))
        
                template_values={'sesion':usur.usuario}
                template = JINJA_ENVIRONMENT.get_template('template/index.html')
                self.response.write(template.render(template_values))                
                
            else:
        
                template_values={'mensaje':'Password incorrecta.'}
                template = JINJA_ENVIRONMENT.get_template('template/login.html')
                self.response.write(template.render(template_values))
        else:
        
            template_values={'mensaje':'Usuario incorrecto.'}
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
        template = JINJA_ENVIRONMENT.get_template('template/registro.html')
        self.response.write(template.render(message=""))

    #Método que registra usuario si pasa las restricciones.

    def post(self):
        
        usuario_introducido = self.request.get('usuario')
        user = model.Usuario()
 
        #Si el usuario no existe, se introducen los datos en la base de datos
        
        if(model.Usuario.query(model.Usuario.usuario == usuario_introducido).get() is None):
            
            user.usuario = self.request.get('usuario')
            user.password = self.request.get('password')
            user.nombre = self.request.get('nombre')
            user.apellido = self.request.get('apellido')
            user.correo = self.request.get('correo')
            user.telefono = self.request.get('telefono')
                        
            user.put()
            self.redirect('/')
            
        else:
             #Si el usuario existe, se muestra un mensaje de error

            self.response.headers['Content-Type'] = 'text/html'
            template = JINJA_ENVIRONMENT.get_template('template/registro.html')
            self.response.write(template.render(message="El nombre de usuario se encuentra en uso"))

#Clase para cambiar los datos de usuario

class editar_perfil(webapp2.RequestHandler):
    
    def get(self):
        
        if self.request.cookies.get("username"):  #Si la cookie está activada
            
            username = str(self.request.cookies.get("username"))
            usuarios = []
            result= model.Usuario.query(model.Usuario.usuario==username)
            
            if result is not None:    #Existe el usuario
                
                for usuario in result:  #Lo buscamos y lo añadimos al array de usuarios
                    
                    usuarios.append(usuario)
                    
                self.response.headers['Content-Type'] = 'text/html'
                template_values = {'usuarios':usuarios,'sesion':username}
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
            template_values={'sesion':username}
            template = JINJA_ENVIRONMENT.get_template('template/error.html')
            self.response.write(template.render(template_values))
            
        else:
            
            self.redirect('/login')

#Clase que gestiona el googlemap de geolocalización
             
class geolocalizacion(webapp2.RequestHandler):
    
    def get(self):
        
        if self.request.cookies.get("username"):
            
            username = str(self.request.cookies.get("username"))
            
            self.response.headers['Content-Type'] = 'text/html'
            template_values={'sesion':username}
            template = JINJA_ENVIRONMENT.get_template('template/geolocalizacion.html')
            self.response.write(template.render(template_values))
            
        else:
            
            self.redirect('/login')

# Clase que genera las coordenadas del dron.

lat = 37.19699469878369
lng =  -3.6241040674591507
grados = 0

class coordenadas(webapp2.RequestHandler):
    
    def get(self):
        
        global lat
        global lng
        global grados

        grados+=5
        lat += 0.00001 * math.cos(grados/180)   #Generación automática de coordenadas provisional
        lng += 0.00001 * math.sin(grados/180)
        latLng = [lat, lng]
        self.response.write(json.dumps(latLng))

#Clase que gestiona el gráfico de monitorización de datos atmosféricos en tiempo real
             
class grafico(webapp2.RequestHandler):
    
    def get(self):
        
        if self.request.cookies.get("username"):
            
            username = str(self.request.cookies.get("username"))
            
            self.response.headers['Content-Type'] = 'text/html'
            template_values={'sesion':username}
            template = JINJA_ENVIRONMENT.get_template('template/grafico.html')
            self.response.write(template.render(template_values))
            
        else:
            
            self.redirect('/login') 
            
# Clase que genera datos aleatorios provisionales para el gráfico
Api_key = 'fffa0ba60d5357235f5782313216b8ae'

class datos_grafico(webapp2.RequestHandler):
    
    def get(self):
        
        global lat
        global lng              #random lat y long
        lat += 0.05
        
        url = 'http://api.openweathermap.org/data/2.5/weather?lat=' + str(lat) + '&lon=' + str(lng) + '&appid=' + Api_key
        response = urllib2.urlopen(url).read()
        r = urllib2.urlopen(url)

        result = json.load(r)
        
        tempe = result["main"]["temp"]          #temperatura
        pres = result["main"]["pressure"]       #presion atmosferica
        hum = result["main"]["humidity"]        #humedad
        vel_wind = result["wind"]["speed"]       #velocidad del viento
        dir_win = result["wind"]["deg"]         #direccion del viento
        
        temp = tempe - 273.15                   #conversion de kelvin a celsius
        vel_win = vel_wind * 3.6                #conversion de m/s a km/h

        dato_seleccionado = self.request.get('dato')

        if dato_seleccionado == 'undefined' or dato_seleccionado == 'Temperatura':
            datoAmostrar = temp;
        elif dato_seleccionado == 'Presion atmosferica':
            datoAmostrar = pres;
        elif dato_seleccionado == 'Humedad':
            datoAmostrar = hum;
        elif dato_seleccionado == 'Velocidad del viento':
            datoAmostrar = vel_win;
        elif dato_seleccionado == 'Direccion del viento':
            datoAmostrar = dir_win;
        
        self.response.write(json.dumps(datoAmostrar)) 

#Clase que gestiona el pronóstico de datos atmosféricos en tiempo real

API_pronostico = 'c6f8c98fd1da5785'
             
class pronostico(webapp2.RequestHandler):
    
    def get(self):
        
        if self.request.cookies.get("username"):
            
            username = str(self.request.cookies.get("username"))
            
            self.response.headers['Content-Type'] = 'text/html'
            template_values={'sesion':username}
            template = JINJA_ENVIRONMENT.get_template('template/pronostico.html')
            self.response.write(template.render(template_values))
            
        else:
            
            self.redirect('/login')   
            
    def post(self):
        
        if self.request.cookies.get("username"):
            
            username = str(self.request.cookies.get("username"))
            
            latitud = self.request.get('latitud')
            longitud = self.request.get('longitud')
            radio_elegido = self.request.get('optradio');
            
            array_datos = []
            error = ''
            latitud_actual = ''
            longitud_actual = ''
            
            try:
                
                if radio_elegido == 'horas':
                    
                    url_horas = 'http://api.wunderground.com/api/' + API_pronostico + '/hourly/conditions/lang:SP/q/' + str(latitud) + ',' + str(longitud) + '.json'
                    
                    response = urllib2.urlopen(url_horas).read()
                    r = urllib2.urlopen(url_horas)
                    result = json.load(r)
                        
                    for i in range(36):                                
                        array_datos.append(result["hourly_forecast"][i])
                                         
                else: 
                    
                    url_dias = 'http://api.wunderground.com/api/' + API_pronostico + '/forecast10day/conditions/lang:SP/q/' + str(latitud) + ',' + str(longitud) + '.json'
    
                    response = urllib2.urlopen(url_dias).read()
                    r = urllib2.urlopen(url_dias)
                    result = json.load(r)
                    
                    for i in range(10):                          
                        array_datos.append(result["forecast"]["simpleforecast"]["forecastday"][i])
                
                latitud_actual = result["current_observation"]["display_location"]["latitude"]
                longitud_actual = result["current_observation"]["display_location"]["longitude"]
                
            except KeyError, e:
                error = 'No existe ninguna ciudad relacionada con esas coordenadas. Por favor consulta "https://www.google.es/maps" para verificar la zona.'
                
            self.response.headers['Content-Type'] = 'text/html'
            template_values={'sesion':username, 
                             'array_datos':array_datos,
                             'radio_elegido':radio_elegido,
                             'latitud_actual':latitud_actual,
                             'longitud_actual':longitud_actual,
                             'error':error
                             }
            
            template = JINJA_ENVIRONMENT.get_template('template/pronostico.html')
            self.response.write(template.render(template_values))
            
        else:
            
            self.redirect('/login')
       
#Obtiene la descripción de cada nubosidad para el METAR

def getInfoNubosidad(nube): 
    
    if(nube == 'SKC'):
        result = 'SKC - Cielo despejado de nubes (sky clear). Cielo limpio por debajo de 12.000 para ASOS/AWOS.'
    elif(nube == 'FEW'):
        result = 'FEW - Nubes escasas. Las nubes cubre entre 1/8 y 2/8 del cielo.'
    elif(nube == 'SCT'):   
        result = 'SCT - Nubes dispersas (scatered). Los nubes cubre entre 3/8 y 4/8 del cielo.' 
    elif(nube == 'BKN'): 
        result = 'BKN - Cielo quebradizo, nubosidad abundante (broken). Las nubes cubren entre 5/8 y 7/8 del cielo.'  
    elif(nube == 'OVC'):
        result = 'OVC - Cielo cubierto (overcast). Cielo totalmente cubierto por nubes.'    
    elif(nube == 'TCU'): 
        result = 'TCU - Desarrollandose cumulonimbos (towering cumulus).'  
    elif(nube == 'CB'):
        result = 'CB - Cumulonimbos (cumulonimbus). Los cumulonimbos son densas formaciones de nubes verticales que pueden provocar fuertes precipitaciones, tormentas eléctricas o granizadas.'
    elif(nube == 'CAVOK'): 
        result = 'CAVOK - Techo y visibilidad OK (Condiciones perfectas para el vuelo)'
        
    return result;

# Clase que genera los datos atmosféricos obtenidos de aeropuertos como son el TAF y METAR

class METAR_TAF(webapp2.RequestHandler):
    
    def get(self):
                    
        global lat
        global lng              #random lat y long
        
        if self.request.cookies.get("username"):
            
            username = str(self.request.cookies.get("username")) 
            error = ''
            array_nubes = []
            array_taf = []
            array_nubes_taf = defaultdict(list)
            taf = ''
            
            try:
                #Gestion del METAR y parseo de la información para su interpretación
                
                url_metar = 'http://avwx.rest/api/metar.php?lat=' + str(lat) + '&lon=' + str(lng) + '&format=JSON'
            
                r_metar = urllib2.urlopen(url_metar)
                result_metar = json.load(r_metar)
                                    
                metar = result_metar["Raw-Report"]
                temperatura = result_metar["Temperature"] + ' grados celsius'
                presion_atmosferica = result_metar["Altimeter"] + ' hPa'
                nubes = result_metar["Cloud-List"]
                
                for nube in nubes:                          #Recorremos el array de nubes obtenidas
                    array_nubes.append(getInfoNubosidad(nube[0]))
   
                fecha_captura = result_metar["Time"]        #Parseo para obtener del string el dia y hora
                dia = fecha_captura[:2]
                hora = fecha_captura[2:4] + ':' + fecha_captura[4:6] + ' UTC'
                
                visibilidad = result_metar["Visibility"] + ' m'
                if visibilidad == '9999 m':                #Si la visibilidad es 9999 significa que hay 10km o mas
                    visibilidad = '10km o mas'
                    
                direccion_viento = result_metar["Wind-Direction"] + ' grados'
                if direccion_viento == '000 grados':       #No hay viento
                    direccion_viento = 'No existe presencia de viento'
                    
                rafaga_viento = result_metar["Wind-Gust"] + ' nudos (KT)'
                
                velocidad_viento = result_metar["Wind-Speed"] + ' nudos (KT)'
                if direccion_viento == '000 nudos (KT)':                #No hay viento
                    direccion_viento = 'No existe presencia de viento'
                
                if rafaga_viento == ' nudos (KT)':
                    rafaga_viento = 'Sin informacion asociada'
                if temperatura == ' grados celsius':
                    temperatura = 'Sin informacion asociada'
                if visibilidad == ' m':
                    visibilidad = 'Sin informacion asociada'
                if direccion_viento == ' grados':
                    direccion_viento = 'Sin informacion asociada'
                if velocidad_viento == ' nudos (KT)':
                    rafaga_viento = 'Sin informacion asociada'
                
                #Gestion del TAF y parseo de alguna de la información para su interpretación. La otra parte esta en el template interpretada
                 
                url_taf = 'http://avwx.rest/api/taf.php?lat=' + str(lat) + '&lon=' + str(lng) + '&format=JSON'
                                                           
                r_taf = urllib2.urlopen(url_taf)
                result_taf = json.load(r_taf)
                
                taf = result_taf["Raw-Report"]
                
                fecha_captura_taf = result_taf["Time"]        #Parseo para obtener del string el dia y hora
                dia_taf = fecha_captura_taf[:2]
                hora_taf = fecha_captura_taf[2:4] + ':' + fecha_captura_taf[4:6]
                
                max_temp = result_taf["Max-Temp"]
                min_temp = result_taf["Min-Temp"]

                for i in range(len(result_taf["Forecast"])):
                    array_taf.append(result_taf["Forecast"][i])
                    
                    for nube in result_taf["Forecast"][i]["Cloud-List"]:               #Recorremos el array de nubes obtenidas
                        array_nubes_taf[i].append(getInfoNubosidad(nube[0]))
            
            except KeyError as e:
                error = 'No es posible verificar la zona por la que va circulando el drone en estos momentos.'
                
            self.response.headers['Content-Type'] = 'text/html'
            template_values={'sesion':username,
                         'error':error, 
                        'metar':metar,
                        'taf':taf,
                        'temperatura':temperatura,
                        'max_temp':max_temp,
                        'min_temp':min_temp,
                        'dia':dia,
                        'hora':hora,
                        'dia_taf':dia_taf,
                        'hora_taf':hora_taf,
                        'array_nubes_taf':array_nubes_taf,
                        'array_nubes':array_nubes,
                        'array_taf':array_taf,
                        'presion_atmosferica':presion_atmosferica,
                        'visibilidad':visibilidad,
                        'direccion_viento':direccion_viento,
                        'rafaga_viento':rafaga_viento,
                        'velocidad_viento':velocidad_viento
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
        ('/datos_grafico', datos_grafico),
        ('/pronostico', pronostico),
        ('/METAR_TAF', METAR_TAF),
        ('/.*', ErrorPage)
       ]

# Creamos la aplicación asignando al URL Dispacher las urls previamente definidas.

application = webapp2.WSGIApplication(urls, debug=True)
    
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
