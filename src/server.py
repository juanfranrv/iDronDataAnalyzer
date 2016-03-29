#!/usr/bin/python
# -⁻- coding: UTF-8 -*-

from google.appengine.ext import ndb
from google.appengine.ext.webapp.util import run_wsgi_app
from collections import defaultdict
from google.appengine.runtime import DeadlineExceededError
from google.appengine.api import urlfetch
import os, model, webapp2, jinja2, json, math, urllib, urllib2, sys, subprocess, random, datetime,time
#import drone_utils

# Declaración del entorno de jinja2 y el sistema de templates.

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#Cabecera y pie de pagina del html

head = JINJA_ENVIRONMENT.get_template('template/head.html').render()
footer = JINJA_ENVIRONMENT.get_template('template/footer.html').render()

#Variables globales

API_pronostico = 'c6f8c98fd1da5785'             #Key para la API del pronóstico
Api_key = 'fffa0ba60d5357235f5782313216b8ae'    #Key para la API del gráfico de monitorización
contador = 0                                    #Variable que lleva la cuenta para la inserción de datos en la base de datos
lat = 37.19699469878369                         #Variables que generan coordenadas aleatorias utilizadas en la mayoría de las clases
lng =  -3.6241040674591507

#Clase que recibe los datos procedentes del HTTP POST de la aplicación de Android y los almacena para ser tratados posteriormente en el resto de funcionalidades

class RecibirDatosDrone(webapp2.RequestHandler):
    
    def post(self):
        
        datosRec = model.DatosRecibidos()
        
        #Obtiene los datos recibidos por Http Post desde el drone (A través de la app de Android)
        latitud = self.request.get('latitud')
        longitud = self.request.get('longitud')
        altura = self.request.get('altura')
        velocidad = self.request.get('velocidad')
        
        busqueda = model.DatosRecibidos.query(model.DatosRecibidos.idDatos == 1).get()
        
        if busqueda is None:    #Si la base de datos está vacía, insertamos los datos recibidos del drone
            
            datosRec.idDatos = 1
            datosRec.latitud = latitud
            datosRec.longitud = longitud
            datosRec.altura = altura
            datosRec.velocidad = velocidad
            
            datosRec.put()
        
        else:                   #Si ya no está vacía, buscamos los únicos datos que tiene y sobreescribimos por los nuevos
            
            busqueda.idDatos = 1
            busqueda.latitud = latitud
            busqueda.longitud = longitud
            busqueda.altura = altura
            busqueda.velocidad = velocidad
            
            busqueda.put()
              
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
        result=model.Usuario.query(model.Usuario.usuario==usu)
        usur=result.get()
        pas=self.request.get('pass')
        
        if usur is not None:

            if usur.password==pas:
                
                self.response.headers.add_header('Set-Cookie',"username="+str(usur.usuario))
        
                template_values={'sesion':usur.usuario,'head':head,'footer':footer}
                template = JINJA_ENVIRONMENT.get_template('template/index.html')
                self.response.write(template.render(template_values))
                                
                self.redirect('/')
                
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
        template_values={'message':"",'head':head}
        template = JINJA_ENVIRONMENT.get_template('template/registro.html')
        self.response.write(template.render(template_values))

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
            result= model.Usuario.query(model.Usuario.usuario == username)
            
            if result is not None:    #Existe el usuario
                
                for usuario in result:  #Lo buscamos y lo añadimos al array de usuarios   
                    usuarios.append(usuario)
                    
                self.response.headers['Content-Type'] = 'text/html'
                template_values = {'usuarios':usuarios,'sesion':username, 'footer': footer,'head':head}
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

#Clase que gestiona el googlemap de geolocalización
             
class geolocalizacion(webapp2.RequestHandler):
    
    def get(self):
        
        if self.request.cookies.get("username"):
            
            username = str(self.request.cookies.get("username"))
            
            datos = model.DatosRecibidos.query(model.DatosRecibidos.idDatos == 1).get()

            lat = datos.latitud
            lng = datos.longitud

            vel = round(float(datos.velocidad),3)
            alt = round(float(datos.altura),3)
 
            self.response.headers['Content-Type'] = 'text/html'
            template_values={'sesion':username,'footer': footer,'head':head,'lat':lat,'lng':lng,'vel':vel,'alt':alt}
            template = JINJA_ENVIRONMENT.get_template('template/geolocalizacion.html')
            self.response.write(template.render(template_values))
            
        else:
            
            self.redirect('/login')

# Clase que genera las coordenadas del dron.

class coordenadas(webapp2.RequestHandler):
    
    def get(self):

        coordenadas = model.DatosRecibidos.query(model.DatosRecibidos.idDatos == 1).get()

        lat = coordenadas.latitud
        lng = coordenadas.longitud
        
        latLng = [lat, lng]
        
        self.response.write(json.dumps(latLng))

#Clase que gestiona la obtención de datos de seguridad en tiempo real

class updateDatosDrone(webapp2.RequestHandler):
    
    def get(self):
        
        datosRec = []
        datos = model.DatosRecibidos.query(model.DatosRecibidos.idDatos == 1).get()
        
        try:

            lat = datos.latitud
            lng = datos.longitud
            
        except:
            
            lat = 37.196                       
            lng =  -3.624
            
        try:
            
            vel = round(float(datos.velocidad),3)
            alt = round(float(datos.altura),3)
            
        except:
            
            vel = 0
            alt = 0
  
        datosRec.append({'latitud': lat,
                         'longitud': lng,
                         'velocidad': vel,
                         'altura': alt
                       })
            
        self.response.write(json.dumps(datosRec))
        
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
        
        global contador
        
        coordenadas = model.DatosRecibidos.query(model.DatosRecibidos.idDatos == 1).get()
        
        lat = coordenadas.latitud
        lng = coordenadas.longitud
        
        data = model.DatosAtmosfericos()
        
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
        
        if contador is 20:               #Cada 10 datos obtenidos, almacenamos en la base de datos
            
            data.fecha = time.strftime("%d-%m-%Y") 
            #Obtiene el número de la semana 
            data.dia = datetime.date.today().strftime("%V")
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
            distancia = 0
            
            if tiempo_elegido == 'mensual':     #Si el tiempo es mensual, comprobamos el mes antes de añadir
                result = model.DatosAtmosfericos.query(model.DatosAtmosfericos.mes == fecha_elegida[3:5], model.DatosAtmosfericos.anio == fecha_elegida[6:11]).order(model.DatosAtmosfericos.fecha)
            
            elif tiempo_elegido == 'semanal':
                num_semana = datetime.date(int(fecha_elegida[6:11]), int(fecha_elegida[3:5]), int(fecha_elegida[0:2])).strftime("%V") 
                result = model.DatosAtmosfericos.query(model.DatosAtmosfericos.dia == num_semana, model.DatosAtmosfericos.anio == fecha_elegida[6:11]).order(model.DatosAtmosfericos.fecha)
                                                
            elif tiempo_elegido == 'anual':     #Si el tiempo es anual, comprobamos el año antes de añadir
                result = model.DatosAtmosfericos.query(model.DatosAtmosfericos.anio == fecha_elegida[6:11]).order(model.DatosAtmosfericos.fecha)

            else:                
                result = model.DatosAtmosfericos.query(model.DatosAtmosfericos.fecha == fecha_elegida)
                
            if result is not None:          
                for dato in result:             #Crear un array de tipo json para parsear en el cliente    
                         datos_atmos.append({'fecha': dato.fecha,
                                            'temperatura': dato.temperatura,
                                            'presion': dato.pres_atmos,
                                            'humedad': dato.humedad,
                                            'vel_viento': dato.vel_viento,
                                            'dir_viento': dato.dir_viento
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
            
            array_datos = []
            error = ''
            latitud_actual = ''
            longitud_actual = ''
            
            try:
                
                if radio_elegido == 'horas':
                    
                    url_horas = 'http://api.wunderground.com/api/' + API_pronostico + '/hourly/conditions/lang:SP/q/' + str(latitud) + ',' + str(longitud) + '.json'
                    
                    r = urllib2.urlopen(url_horas)
                    result = json.load(r)
                        
                    for i in range(36):                                
                        array_datos.append(result["hourly_forecast"][i])
                                         
                else: 
                    
                    url_dias = 'http://api.wunderground.com/api/' + API_pronostico + '/forecast10day/conditions/lang:SP/q/' + str(latitud) + ',' + str(longitud) + '.json'
    
                    r = urllib2.urlopen(url_dias)
                    result = json.load(r)
                    
                    for i in range(10):                          
                        array_datos.append(result["forecast"]["simpleforecast"]["forecastday"][i])
                
                latitud_actual = result["current_observation"]["display_location"]["latitude"]
                longitud_actual = result["current_observation"]["display_location"]["longitude"]
                
            except KeyError, e:
                error = 'No existe ninguna ciudad relacionada con esas coordenadas. Por favor, verifique la zona.'
                
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
        result = 'SKC - Cielo despejado de nubes a ' + altura + '00 pies (sky clear). Cielo limpio por debajo de 12.000 para ASOS/AWOS.'
    elif nube == 'FEW':
        result = 'FEW - Nubes escasas a ' + altura + '00 pies. Las nubes cubre entre 1/8 y 2/8 del cielo.'
    elif nube == 'SCT':   
        result = 'SCT - Nubes dispersas a ' + altura + '00 pies (scatered). Los nubes cubre entre 3/8 y 4/8 del cielo.' 
    elif nube == 'BKN': 
        result = 'BKN - Cielo quebradizo, nubosidad abundante a  ' + altura + '00 pies (broken). Las nubes cubren entre 5/8 y 7/8 del cielo.'  
    elif nube == 'OVC':
        result = 'OVC - Cielo cubierto a ' + altura + '00 pies (overcast). Cielo totalmente cubierto por nubes.'    
    elif nube == 'TCU': 
        result = 'TCU - Desarrollandose cumulonimbos a ' + altura + '00 pies  (towering cumulus).'  
    elif nube == 'CB':
        result = 'CB - Cumulonimbos a ' + altura + '00 pies (cumulonimbus). Los cumulonimbos son densas formaciones de nubes verticales que pueden provocar fuertes precipitaciones, tormentas eléctricas o granizadas.'
    elif nube == 'CAVOK': 
        result = 'CAVOK - Techo y visibilidad OK a ' + altura + '00 pies  (Condiciones perfectas para el vuelo)'
        
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
    datos_metar = []

    #Inicio del parseo
    metar = result_metar["Raw-Report"]
    temperatura = result_metar["Temperature"] + ' grados celsius'
    presion_atmosferica = result_metar["Altimeter"] + ' hPa'
    nubes = result_metar["Cloud-List"]
     
    for nube in nubes:                          #Recorremos el array de nubes obtenidas
        array_nubes.append(getInfoNubosidad(nube[0], nube[1]))

    fecha_captura = result_metar["Time"]        #Parseo para obtener del string el dia y hora
    dia = fecha_captura[:2]
    hora = fecha_captura[2:4] + ':' + fecha_captura[4:6] + ' UTC'
     
    visibilidad = result_metar["Visibility"] + ' m'
    if visibilidad == '9999 m':                #Si la visibilidad es 9999 significa que hay 10km o mas
        visibilidad = '10km o mas'
         
    direccion_viento = result_metar["Wind-Direction"] + ' grados'
    if direccion_viento == '000 grados':       #No hay viento
        direccion_viento = 'No existe presencia de viento'
    elif direccion_viento == "VRB grados":
        direccion_viento = 'Viento en todas las direcciones'
         
    rafaga_viento = result_metar["Wind-Gust"] + ' nudos (KT)'
     
    velocidad_viento = result_metar["Wind-Speed"] + ' nudos (KT)'
    if velocidad_viento == '00 nudos (KT)':                #No hay viento
        velocidad_viento = 'No existe presencia de viento'
     
    if len(array_nubes) is 0:
        array_nubes.append('Sin informacion asociada')
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
     
    #Devolución de JSON con los datos parseados      
    datos_metar.append({'presion_atmosferica':presion_atmosferica,
                        'visibilidad':visibilidad,
                        'direccion_viento':direccion_viento,
                        'rafaga_viento':rafaga_viento,
                        'velocidad_viento':velocidad_viento,
                        'temperatura':temperatura,
                        'metar':metar,
                        'array_nubes':array_nubes,
                        'dia':dia,
                        'hora':hora,
                       })
    
    return datos_metar

#Parsea la información obtenida (no repetida) y devuelve un JSON con el TAFOR legible

def parseoTAFOR_noRepeatInfo(result_taf):

    #Inicialización de variables
    datos_taf = []
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
        max_temp = "Sin informacion asociada"
    else:
        max_temp = max_temp[2:4]
      
    if min_temp == '':
        min_temp = "Sin informacion asociada"
    else:
        min_temp = min_temp[2:4] 
        
    for i in range(len(result_taf["Forecast"])):
        
        for nube in result_taf["Forecast"][i]["Cloud-List"]:    #Recorremos el array de nubes obtenidas
            array_nubes_taf[i].append(getInfoNubosidad(nube[0], nube[1]))

    #Devolución de JSON con los datos parseados  
    datos_taf.append({'taf':taf,
                      'max_temp':max_temp,
                      'min_temp':min_temp,
                      'dia_taf':dia_taf,
                      'hora_taf':hora_taf,
                      'array_nubes_taf':array_nubes_taf
                    })

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
            presion = 'Sin informacion asociada'
        else:
            presion = taf["Altimeter"] + ' hPa'
            
        if taf["Visibility"] == '9999':
            visibilidad = '10km o superior'
        elif taf["Visibility"] == '':
            visibilidad = 'Sin informacion asociada'
        else:
            visibilidad = taf["Visibility"] + ' m'
            
        if taf["Wind-Direction"] == '':
            dir_viento = 'Sin informacion asociada'
        elif taf["Wind-Direction"] == 'VRB':
            dir_viento = 'Viento en todas las direcciones'
        else:
            dir_viento = taf["Wind-Direction"] + ' grados'
            
        if taf["Wind-Gust"] == '':
            rafaga_viento = 'Sin informacion asociada'
        else:
            rafaga_viento = taf["Wind-Gust"] + ' nudos (KT)'
            
        if taf["Wind-Speed"] == '':
            vel_viento = "Sin informacion asociada"
        else:
            vel_viento = taf["Wind-Speed"] + ' nudos (KT)'

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
        
        coordenadas = model.DatosRecibidos.query(model.DatosRecibidos.idDatos == 1).get()
        
        lat = coordenadas.latitud
        lng = coordenadas.longitud
        
        if self.request.cookies.get("username"):
            
            #Inicialización de variables para que siga funcionando en el que caso de que no exista alguna
            
            username = str(self.request.cookies.get("username")) 
            error = ''
            array_metar = []
            array_taf = []
            array_tafN = []
            
            try:
                #Gestión del METAR y parseo de la información para su interpretación
                
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
                
            except KeyError, e:
                error = 'No es posible verificar la zona por la que va circulando el drone en estos momentos.'
                
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
        ('/updateDatosDrone', updateDatosDrone),
        ('/METAR_TAF', METAR_TAF),
        ('/.*', ErrorPage)
       ]

# Creamos la aplicación asignando al URL Dispacher las urls previamente definidas.

application = webapp2.WSGIApplication(urls, debug=True)
    
def main():
    run_wsgi_app(application)
    #drone_utils.conexion_drone()

if __name__ == "__main__":
    main()
