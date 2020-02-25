import json
import requests
import urllib3

from providers.base.casadecambio import CasaDeCambio
from providers.base.origintype import OriginType
from base.cotizacion import Cotizacion

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Cambioschaco(CasaDeCambio):   #Se cambia el nombre a Cambioschaco debido a error de import

    __id = "cambioschaco"
    name = "Cambios Chaco"
    #originType = OriginType.JSON
    #header = ""
    #data = ""

    sucursales = [
            {"id": "adrian-jara", "name": "Adrián Jara", "loc": "LatLng", "idSuc": "9"},
            {"id": "km4", "name": "Supercarretera Km 4", "loc": "LatLng", "idSuc": "10"},
            {"id": "itay-bate", "name": "Itá Ybate", "loc": "LatLng", "idSuc": "11"},
            {"id": "km7", "name": "Km 7", "loc": "LatLng", "idSuc": "12"},
            {"id": "noblesse", "name": "Noblesse Km 3,5", "loc": "LatLng", "idSuc": "13"},
            {"id": "curupayty", "name": "Curupayty", "loc": "LatLng", "idSuc": "14"},
            {"id": "ciudad-nueva", "name": "Agencia Ciudad Nueva", "loc": "LatLng", "idSuc": "32"},
        ]

    def getSucursales(self):
        """Devuelve un dict con todas las sucursales que tienen cotizaciones listadas en la web"""
        return {
            self.__id : { "sucursales": self.sucursales }
        }

    def getURL(self, idSuc):
        return f"https://www.cambioschaco.com.py/api/branch_office/{idSuc}/exchange"

    def getCotizacionSucursal(self, url):
        compraVenta = Cotizacion(0,0)
        try:
            jsontext = json.loads(
                requests.get(url,timeout=10,verify=False).text
            )
            compra = jsontext["items"][0]["purchasePrice"]
            venta = jsontext["items"][0]["salePrice"]
            compraVenta = Cotizacion(compra, venta)
        except requests.ConnectionError as e:
            #ToDo: hacer logging
            print("Connection error: ")
            print(e)
        except:
            #ToDo: ser más específico
            print("Another error")

        return compraVenta
    
    
    def getCotizaciones(self):
        """Devuelve un dict con todas las cotizaciones de la entidad, por sucursal"""
        cotizaciones_dict = {}

        for suc in self.sucursales:
            url = self.getURL(suc['idSuc'])

            cambioEnSucursal = self.getCotizacionSucursal(url)
            
            cotizaciones_dict[suc['id']] = cambioEnSucursal.getValuesDict()
        
        return { self.__id : cotizaciones_dict }


    def test(self):
        cc = CambiosChaco()
        #sucursales
        suc = cc.getSucursales()
        print(json.dumps(suc, indent=4))

        #cotizaciones
        coti = cc.getCotizaciones()
        #print(coti)
        print(json.dumps(coti, indent=4))
