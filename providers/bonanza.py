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

class Bonanza(CasaDeCambio):

    __id = "bonanza"
    name = "Bonanza Cambios"
    originType = OriginType.HTML
    #header = ""
    #data = ""

    sucursales = [
            {"id": "casa-matriz", "name": "Casa Matriz", "loc": "", "index": 0},
            {"id": "edif-saba", "name": "Edificio Saba", "loc": "", "index": 1},
            {"id": "jebai", "name": "Jebai", "loc": "", "index": 2},
            {"id": "internacional", "name": "Internacional", "loc": "", "index": 3},
            {"id": "pcc", "name": "Paraná Country Club", "loc": "", "index": 4},
        ]

    def getSucursales(self):
        """Devuelve un dict con todas las sucursales que tienen cotizaciones listadas en la web"""
        return {
            self.__id : { "sucursales": self.sucursales }
        }

    def getCotizacionesWeb(self):
        compra = 0
        venta = 0
        cambio = Cotizacion(compra, venta)
        cotizacionesDict = {}

        try:
            soup = BeautifulSoup(
                requests.get('https://bonanzacambios.com.py', timeout=10,
                            headers={'user-agent': 'Mozilla/5.0'}, verify=False).text, "html.parser")

            #table-pricing style1 > table > tbody > tr > td(flag), td(title --ej: Dolar Americano), td(moneda,compra), td (+=-), td(moneda,venta)
            #<!-- /.tab-0 MATRIZ -->
            # <!-- /.tab-1 SABA -->
            # <!-- /.tab-2 JEBAI -->
            # <!-- /.tab-0 INTER -->
            # <!-- /.tab-4 PARANA -->
            tablaCambio = soup.select('div.table-pricing.style1')
            for sucursal in self.sucursales:
                monedas = tablaCambio[sucursal['index']].select('.moneda')
                compra = int(monedas[0].get_text().replace('.', ''))
                venta = int(monedas[1].get_text().replace('.', ''))
                cambio = Cotizacion(compra, venta)
                cotizacionesDict.update({sucursal['id']: cambio.getValuesDict()})


        except requests.ConnectionError as e:
            #ToDo: hacer logging
            print("Connection error: ")
            print(e)
        except:
            #ToDo: ser más específico
            print("Another error")

        return cotizacionesDict
    
    def getCotizaciones(self):
        """Devuelve un dict con todas las cotizaciones de la entidad, por sucursal"""
        return { self.__id : self.getCotizacionesWeb()}


    def test(self):
        cc = Bonanza()
        #sucursales
        suc = cc.getSucursales()
        print(json.dumps(suc, indent=4))

        #cotizaciones
        coti = cc.getCotizaciones()
        #print(coti)
        print(json.dumps(coti, indent=4))

if __name__ == '__main__':
    Bonanza.test(None)