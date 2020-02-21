import json
import requests
import urllib3
from bs4 import BeautifulSoup

from providers.base.casadecambio import CasaDeCambio
from providers.base.origintype import OriginType
from base.cotizacion import Cotizacion

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Vision(CasaDeCambio):

    __id = "vision"
    name = "Vision Banco"
    originType = OriginType.HTML
    #header = ""
    #data = ""

    sucursales = [
            {"id": "web", "name": "Cotización de la Web", "loc": ""},
        ]

    def getSucursales(self):
        return {
            self.__id : { "sucursales": self.sucursales }
        }

    def getCotizacionVisionWeb(self):
        cambio = Cotizacion(0, 0)

        try:
            soup = BeautifulSoup(
                requests.get('https://www.visionbanco.com', timeout=10,
                            headers={'user-agent': 'Mozilla/5.0'}, verify=False).text, "html.parser")

            efectivo = soup.select('#efectivo')[0]
            compra = efectivo.select('table > tr > td:nth-of-type(2) > p:nth-of-type(1)')[0].get_text().replace('.', '')
            venta = efectivo.select('table > tr > td:nth-of-type(3) > p:nth-of-type(1)')[0].get_text().replace('.', '')
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
        return { self.__id : {self.sucursales[0]['id'] : self.getCotizacionVisionWeb().getValuesDict()} }


    def test(self):
        cc = Vision()
        #sucursales
        suc = cc.getSucursales()
        print(json.dumps(suc, indent=4))

        #cotizaciones
        coti = cc.getCotizaciones()
        #print(coti)
        print(json.dumps(coti, indent=4))
