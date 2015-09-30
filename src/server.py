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
             #Si el usuario existe, se muestra mensaje de error

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
            
            if result>0:    #Existe el usuario
                
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
                    
                    us.password = self.request.get('password')
                    us.nombre = self.request.get('nombre')
                    us.apellido = self.request.get('apellido')
                    us.correo = self.request.get('correo')
                    us.telefono = self.request.get('telefono')
                            
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
            
# Urls de la aplicación con sus clases asociadas.

urls = [('/', MainPage),
        ('/login', Login),
        ('/formRegistro',formRegistro),
        ('/logout', cerrar_sesion),
        ('/editar_perfil', editar_perfil),
        ('/.*', ErrorPage)
       ]

# Creamos la aplicación asignando al URL Dispacher las urls previamente definidas.

application = webapp2.WSGIApplication(urls, debug=True)
    
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
