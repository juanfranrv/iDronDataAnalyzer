#!/usr/bin/python
# -⁻- coding: UTF-8 -*-

from google.appengine.ext import ndb
from google.appengine.ext.webapp.util import run_wsgi_app
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
        lng += 0.05
        
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
        vel_win = vel_wind + 3.6                #conversion de m/s a km/h

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

            if radio_elegido == 'horas':
                
                url_horas = 'http://api.wunderground.com/api/' + API_pronostico + '/hourly/lang:SP/q/' + str(latitud) + ',' + str(longitud) + '.json'

                response = urllib2.urlopen(url_horas).read()
                r = urllib2.urlopen(url_horas)
                result = json.load(r)
                
                for i in range(36):
                    
                    array_datos.append(result["hourly_forecast"][i])
                
            else: 
                
                url_dias = 'http://api.wunderground.com/api/' + API_pronostico + '/forecast10day/lang:SP/q/' + str(latitud) + ',' + str(longitud) + '.json'

                response = urllib2.urlopen(url_dias).read()
                r = urllib2.urlopen(url_dias)
                result = json.load(r)

                for i in range(10):
                                        
                    array_datos.append(result["forecast"]["simpleforecast"]["forecastday"][i])
            
            self.response.headers['Content-Type'] = 'text/html'
            template_values={'sesion':username, 
                             'array_datos':array_datos,
                             'radio_elegido':radio_elegido
                             }
            
            template = JINJA_ENVIRONMENT.get_template('template/pronostico.html')
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
        ('/.*', ErrorPage)
       ]

# Creamos la aplicación asignando al URL Dispacher las urls previamente definidas.

application = webapp2.WSGIApplication(urls, debug=True)
    
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
