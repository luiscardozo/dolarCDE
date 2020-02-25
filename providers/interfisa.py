import json
import requests
import urllib3
from bs4 import BeautifulSoup

from base.casadecambio import CasaDeCambio
from base.origintype import OriginType
from base.cotizacion import Cotizacion

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Interfisa(CasaDeCambio):

    __id = "interfisa"
    name = "Interfisa Banco"
    originType = OriginType.JSON
    #header = ""
    #data = ""

    sucursales = [
            {"id": "web", "name": "Cotización de la Web", "loc": ""},
        ]

    def getSucursales(self):
        return {
            self.__id : { "sucursales": self.sucursales }
        }

    def getCotizacionWeb(self):
        compra = 0
        venta = 0
        cambio = Cotizacion(compra, venta)

        try:
            jsonResult = requests.get(
                "https://seguro.interfisa.com.py/rest/cotizaciones", timeout=10
            ).json()
            cotizaciones = jsonResult["operacionResponse"]["cotizaciones"]["monedaCot"]
            for coti in cotizaciones:
                for k, v in coti.items():
                    if v == "DOLARES AMERICANOS":  # estamos en el dict de Dolares
                        compra = coti["compra"]
                        venta = coti["venta"]

            cambio = Cotizacion(compra, venta)

        except requests.ConnectionError as e:
            #ToDo: hacer logging
            print("Connection error: ")
            print(e)
        except:
            #ToDo: ser más específico
            print("Another error")

        return cambio
    
    def getCotizaciones(self):
        return { self.__id : {self.sucursales[0]['id'] : self.getCotizacionWeb().getValuesDict()} }


    def test(self):
        ib = Interfisa()
        #sucursales
        suc = ib.getSucursales()
        print(json.dumps(suc, indent=4))

        #cotizaciones
        coti = ib.getCotizaciones()
        #print(coti)
        print(json.dumps(coti, indent=4))
