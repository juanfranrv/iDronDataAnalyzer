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
import sys
import subprocess

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
            
#Clase para gestionar el logueo del usuario.

class Login(webapp2.RequestHandler):
    
    def get(self):
            
            self.response.headers['Content-Type'] = 'text/html'
            template_values={}
            template = JINJA_ENVIRONMENT.get_template('template/login.html')
            self.response.write(template.render(template_values))
            
    #Implementa el login de usuarios guardando la sesión en una cookie.
    
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

    #Método que registra al usuario si pasa las restricciones.

    def post(self):
        
        usuario_introducido = self.request.get('usuario')
        user = model.Usuario()
 
        #Si no aparece se cogen los datos introducidos en el formulario y se introducen en la base de datos
        
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
             #Si el usuario aparece, se muestra mensaje de error: usuario existente

            self.response.headers['Content-Type'] = 'text/html'
            template = JINJA_ENVIRONMENT.get_template('template/registro.html')
            self.response.write(template.render(message="El nombre de usuario se encuentra en uso"))
            
# Urls de la aplicación con sus clases asociadas.

urls = [('/', MainPage),
        ('/login', Login),
        ('/formRegistro',formRegistro),
        ('/logout', cerrar_sesion),
        #('/.*', ErrorPage)
       ]

# Creamos la aplicación asignando al URL Dispacher las urls previamente definidas.

application = webapp2.WSGIApplication(urls, debug=True)

# Declaración del entorno de jinja2 y el sistema de templates.

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# Despliega la aplicación al ejecutar el archivo como script. 
    
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
