import json
import requests
import urllib3
from bs4 import BeautifulSoup

if __name__ == '__main__':
    import sys
    sys.path.append(sys.path[0] + '/..')

from base.casadecambio import CasaDeCambio
from base.origintype import OriginType
from base.cotizacion import Cotizacion

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Alberdi(CasaDeCambio):

    __id = "alberdi"
    name = "Cambios Alberdi"
    originType = OriginType.JSON
    #header = ""
    #data = ""

    sucursales = [
            {"id": "cde", "name": "Ciudad del Este", "loc": ""},
            {"id": "cde2", "name": "Ciudad del Este2", "loc": ""},
            {"id": "km4", "name": "Ciudad del Este - Km 4", "loc": ""},
        ]

    def getSucursales(self):
        return {
            self.__id : { "sucursales": self.sucursales }
        }

    def getCotizacionesWeb(self, moneda = "USD"):
        compra = 0
        venta = 0
        cambio = Cotizacion(compra, venta)
        idMoneda = 0

        cotizacionesDict = {}

        try:
            url = "http://cambiosalberdi.com/ws/getCotizaciones.json"
            jsonStr = requests.get(url, timeout=10).json()
            moneda = 0 #dolar
            for sucursal in self.sucursales:
                compra = jsonStr[sucursal['id']][idMoneda]["compra"].replace(".", "")
                venta = jsonStr[sucursal['id']][idMoneda]["venta"].replace(".", "")
                cambio = Cotizacion(int(compra), int(venta))
                cotizacionesDict.update({sucursal['id']: cambio.getValuesDict()})

        except requests.ConnectionError as e:
            #ToDo: hacer logging
            print("Connection error: ")
            print(e)
        #except:
            #ToDo: ser más específico
        #    print("Another error")

        return cotizacionesDict
    
    def getCotizaciones(self):
        return { self.__id : self.getCotizacionesWeb() }


    def test(self):
        ib = Alberdi()
        #sucursales
        suc = ib.getSucursales()
        print(json.dumps(suc, indent=4))

        #cotizaciones
        coti = ib.getCotizaciones()
        #print(coti)
        print(json.dumps(coti, indent=4))

if __name__ == '__main__':
    Alberdi.test(None) #Cómo lo hago "static" ?
