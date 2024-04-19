#import respuesta
#import re
#from xmlrpc.client import boolean
#from colorama import reinit
import json
import pdb
from flask import *
from flask_restful import Resource, Api

#from sqlalchemy import create_engine, false, true
#from secrets import choice


app = Flask(__name__)
api = Api(app)

@app.route('/')
def home():
   return render_template('front.html')

@app.route('/js/app.js')
def js():
   return send_file('js/app.js')


class fCalcula(Resource):
    
    #Calcula cuantas veces cabe el rectangulo a,b dentro del rectangulo x,y
    def get(self):
        lado_a = int(request.args.get('lado_a'))
        lado_b = int(request.args.get('lado_b'))
        lado_x = int(request.args.get('lado_x'))
        lado_y = int(request.args.get('lado_y'))
        
        #primero calculo con el rectangulo ab en posicion original
        respuestaAB = self.setRespuesta('ab', lado_a, lado_b, lado_x, lado_y)
        #luego calculo con cambio en la orientación
        respuestaBA = self.setRespuesta('ba', lado_b, lado_a, lado_x, lado_y)
        
        #finalmente, retorno la opción que mas rectangulos entregue, si son iguales retorno orientacion original.
        if respuestaAB.cantidadRectangulos()< respuestaBA.cantidadRectangulos():
            return to_json(respuestaBA)
        else:
            #return lado_a
            return to_json(respuestaAB)

    def setRespuesta(self, orientacion, lado_c, lado_d, lado_x, lado_y):
        #pdb.set_trace()
        res = respuesta()
        res.orientacion = orientacion
        
        #primero calculo cuantas veces cabe el rectangulo orientado con a (& x)como ancho
        cols = int(lado_x / lado_c)
        filas = int(lado_y / lado_d)
        resto_cols = 0
        resto_filas = 0
        #valido que rectangulo cabe
        if cols>0 and filas>0:
            #Luego veo si en el resto caben mas rectangulos a,b cambiando la orientación

            #Si el ancho es menor al alto, no caben rectangulos en el espacio sobrante del ancho, por lo que el cálculo 
            #se debe realizar en el sobrante del eje y
            if lado_c<lado_d:
                resto_y = lado_y - (filas * lado_d)
                if resto_y>0:
                    resto_cols = int(lado_x / lado_d)
                    resto_filas = int(resto_y / lado_c)
            else:
                #Si el ancho es mayor al alto, no caben rectangulos en el espacio sobrante del alto, por lo que el cálculo 
                #se debe realizar en el sobrante del eje x
                if lado_c>lado_d:
                    resto_x = lado_x - (cols * lado_c)
                    if resto_x>0:
                        resto_cols = int(resto_x / lado_d)
                        resto_filas = int(lado_y  / lado_c)
            
        res.cols= cols 
        res.filas = filas
        res.colsResto = resto_cols
        res.filasResto = resto_filas
        
        return res


class respuesta:
    def __init__(self) -> None:
        self.orientacion = 'ab'
        self.cols = 0 #Cantidad de columnas del rectangulo con el lado de ancho definido en ladoAnchoIni
        self.filas = 0 #Cantidad de columnas del rectangulo con el lado de ancho definido en ladoAnchoIni
        self.colsResto = 0 #Cantidad de columnas del rectangulo con el lado de ancho contrario al definido en ladoAnchoIni
        self.filasResto = 0 #Cantidad de columnas del rectangulo con el lado de ancho definido contrario al en ladoAnchoIni

    def cantidadRectangulos(self):
       return (self.filas * self.cols) + (self.filasResto * self.colsResto)

def to_json(obj):
    return json.dumps(obj, default=lambda obj: obj.__dict__) 



    
api.add_resource(fCalcula, '/fCalcula') 

if __name__ == '__main__':
     app.run(port='5000')        

