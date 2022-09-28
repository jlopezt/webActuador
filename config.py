import json

OK                          =  0
CONFIGURACION_POR_DEFECTO   = -1
ERROR_FICHERO_CONFIGURACION = -2
INICIAL                     = -100

class Configuracion:
    __IP = 0
    __puerto = 0
    __outputFile = ''
    __Apps =0
    __configurado = INICIAL

    def __init__(self, fichero, debug = False, IP = "0.0.0.0",puerto = "0",outputFile='salida.log', dbIP = "0.0.0.0",dbPuerto = 0,baseDatos = '',measurement = ''):
        #valores por defecto sobre el bus MQTT
        __IP = IP
        __puerto = puerto
        __outputFile = outputFile

        #valores por defecto sobre las Apps
        #__Apps[] = dbIP

        self.__leeConfiguracion(fichero,debug)

    def __leeConfiguracion(self,fichero,debug=False):
        if (debug==True): print("\nInicio de configuracion----------------------------------------------------------------------")
        self.__configurado = OK #por defecto va bien...

        try:
            #leo el fichero de configuracion
            with open(fichero) as json_file:
                configuracion = json.load(json_file)
                if (debug==True): print("Configuracion leida=\n %s" %configuracion)
        except :
            if (debug==True): print("No se pudo obtener el fichero de configuracion")
            self.__configurado = ERROR_FICHERO_CONFIGURACION
            return

        if configuracion.has_key('Proceso'): 
            proceso = configuracion['Proceso']

            if proceso.has_key('IP'): self.setIP(proceso.pop("IP"))
            else: 
                if (debug==True): 
                    print("IP no esta configurado. Valor por defecto.")
                    self.__configurado = CONFIGURACION_POR_DEFECTO

            if proceso.has_key('puerto'): self.setPuerto(proceso.pop("puerto"))
            else: 
                if (debug==True): 
                    print("puerto no esta configurado. Valor por defecto.")
                    self.__configurado = CONFIGURACION_POR_DEFECTO

            if proceso.has_key('outputFile'): self.setOutputFile(proceso.pop("outputFile"))
            else: 
                if (debug==True): 
                    print("outputFile no esta configurado. Valor por defecto.")
                    self.__configurado = CONFIGURACION_POR_DEFECTO
        else: 
            if (debug==True): 
                print("No se ha configurado el proceso. Valores pore defecto")
                self.__configurado = CONFIGURACION_POR_DEFECTO

        if configuracion.has_key('Apps'): 
            __Apps = dict(configuracion['Apps'])
        else:
            if (debug==True): 
                print("No se ha configurado Apps. Valores pore defecto")
                self.__configurado = CONFIGURACION_POR_DEFECTO

        if (debug==True): print("Configuracion del proceso")
        if (debug==True): print("IP = %s" %self.__IP)
        if (debug==True): print("puerto = %s" %self.__puerto)
        if (debug==True): print("outputFile = %s" %self.__outputFile)

    def setIP(self,valor): self.__IP=str(valor)
    def setPuerto(self,valor): self.__puerto=valor
    def setOutputFile(self,valor): self.__outputFile=valor

    def getIP(self): return self.__IP
    def getPuerto(self): return self.__puerto
    def getOutputFile(self): return self.__outputFile    

    def getConfigurado(self): return self.__configurado