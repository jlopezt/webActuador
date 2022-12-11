#from typing import final
from flask import Flask, render_template, request, redirect
from markupsafe import escape

import requests as outputRequests
import json
import sys

import config

#declaracion de variables globales
configFile='config/config.json'
parametro=""

app = Flask(__name__)

@app.route('/')
def raiz():
    print('Pagina principal',sys.stderr)
    with open(configFile) as json_file:
        configuracion = json.load(json_file)

        #Leo la configuracion
        raiz=configuracion["Raiz"]
        nombre=raiz["nombre"]
        cabecera = raiz["cabecera"]
        pie = raiz["pie"]
        apps = configuracion["Apps"]
        
        print('cabecera: ' + cabecera + ' longitud=' + str(len(cabecera)),sys.stderr)
        print('pie: ' + pie,sys.stderr)

        #nombre
        i=0
        nombrePrincipio=""
        while i<(len(nombre)-3):
            nombrePrincipio += nombre[i]
            i = i + 1

        print('Nombre principio: ' + nombrePrincipio,sys.stderr)

        nombreRojo=nombre[len(nombre)-3]
        print('rojo: ' + nombreRojo,sys.stderr)
        nombreFinal=nombre[len(nombre)-2]+nombre[len(nombre)-1]
        print('final: ' + nombreFinal,sys.stderr)

        #cabecera
        i=0
        principio=""
        while i<(len(cabecera)-3):
            principio += cabecera[i]
            i = i + 1

        print('principio: ' + principio,sys.stderr)

        rojo=cabecera[len(cabecera)-3]
        print('rojo: ' + rojo,sys.stderr)
        final=cabecera[len(cabecera)-2]+cabecera[len(cabecera)-1]
        print('final: ' + final,sys.stderr)

        return render_template('index.html', NOMBRE_PRINCIPIO=nombrePrincipio, NOMBRE_ROJO=nombreRojo, NOMBRE_FINAL=nombreFinal, PRINCIPIO=principio, ROJO=rojo, FINAL=final, PIE=pie, APPS=apps)

@app.route('/paneles/')
def paneles():
    print('Pagina de paneles',sys.stderr)
    with open(configFile) as json_file:
        configuracion = json.load(json_file)

        #Leo la configuracion
        apps =configuracion["Apps"]
        return render_template('paneles.html', NUM_APPS=len(apps), APPS=apps)
 
@app.route('/<dispositivo>/')
def cacharro(dispositivo):
#    try:
        #leo el fichero de configuracion
        print('DISPOSITIVO dispositivo: ' + dispositivo,sys.stdout)

        with open(configFile) as json_file:
            configuracion = json.load(json_file)
            Proceso=configuracion.get('Proceso')
            Ip=Proceso['IP']

            Apps=configuracion.get('Apps')
            #print('Configuracion Apps=\n nombre: ', Apps[1]['nombre'],' IP: ', Apps[1]['IP'], '\n\n', file=sys.stdout)
            for x in Apps:
                if(x['nombre']==dispositivo):
                    print('Encontrado!! IP: ', x['IP'], sys.stdout)
                    IPDispositivo=x['IP']
                    print('IPDispositivo: ' + IPDispositivo, sys.stdout)
                    return render_template('main.html', IP=Ip, IPDISPOSITIVO=IPDispositivo, DISPOSITIVO=dispositivo)                    

            print('App no configurada',sys.stdout)
            return f'<p>App no configurada</p>'
          
            return f'<p>Hello, World!<br>We are in {escape(dispositivo)}!!!!!</p><BR> se han configrado'
#    except :
#        print("No se pudo obtener el fichero de configuracion")            
#        return f'Algo salio mal...'

@app.route('/<dispositivo>/<recurso>')
def ficheros(dispositivo,recurso):
#    try:
        #leo el fichero de configuracion
        print('SERVICIO: dispositivo: ' + dispositivo + ' | recurso: ' + recurso + '@',sys.stderr)

        with open(configFile) as json_file:
            configuracion = json.load(json_file)
            Proceso=configuracion.get('Proceso')
            Ip=Proceso['IP']
            puerto=Proceso['puerto']

            Apps=configuracion.get('Apps')
            for x in Apps:
                if(x['nombre']==dispositivo):
                    IPDispositivo=x['IP']

                    Paginas=x['Paginas']
                    for p in Paginas:
                        if(p['nombre']==recurso):
                            pagina=p['pagina']
                            print('Encontrada pagina: ' + recurso + ' | pagina: ' + pagina, sys.stderr)
                            return render_template(pagina, IP=Ip, IPDISPOSITIVO=IPDispositivo, DISPOSITIVO=dispositivo)

                    print('Recurso no encontrado como pagina: ' + recurso, sys.stderr)
                    #Leo los parametros y redirecciono
                    parametros=""
                    for param in request.args:
                        if parametros!="": parametros += "&"
                        valor=request.args[param]
                        parametros += param + "=" + valor

                    Servicios=x['Servicios']
                    for s in Servicios:
                        if(s['nombre']==recurso):
                            servicio=s['servicio']
                            print('Encontrado servicio: ' + recurso + ' | servicio: ' + servicio, sys.stderr)
                            return redirect('http://'+IPDispositivo+'/'+servicio+'?'+parametros, code=302)

                    print('Recurso no encontrado como servicio: ' + recurso, sys.stdout)

                    #Envio error 404
                    return redirect('http://' + Ip + ':' + str(puerto) + '/static/404.html', code=302)

            print('App no configurada',sys.stdout)
            return f'<p>App no configurada</p>'
#    except :
#        print("No se pudo obtener el fichero de configuracion")            
#        return f'Algo salio mal...'
