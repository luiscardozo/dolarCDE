import json
import requests
import urllib3

#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# PACKAGE_PARENT = '..'
# SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
# sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from providers.base.casadecambio import CasaDeCambio
from providers.base.origintype import OriginType
from lib.cotizacion import Cotizacion

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CambiosChaco(CasaDeCambio):

    ident = "cambioschaco"
    name = "Cambios Chaco"
    originType = OriginType.JSON
    header = ""
    data = ""

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
        return {
            self.ident : { "sucursales": self.sucursales }
        }

    def getURL(self, idSuc):
        return f"https://www.cambioschaco.com.py/api/branch_office/{idSuc}/exchange"

    def getCotizacionSucursal(self, url):
        compraVenta = Cotizacion(0,0)
        try:
            soup = json.loads(
                requests.get(url,timeout=10,verify=False).text
            )
            compra = soup["items"][0]["purchasePrice"]
            venta = soup["items"][0]["salePrice"]
            compraVenta = Cotizacion(compra, venta)
        except requests.ConnectionError as e:
            print("Connection error: ")
            print(e)
        except:
            print("Another error")

        return compraVenta
        
    def getCotizaciones(self):
        cotizaciones = {}

        for suc in self.sucursales:
            url = self.getURL(suc['idSuc'])

            cambioEnSucursal = self.getCotizacionSucursal(url)
            #print(f"{suc['id']}: {cambioEnSucursal}")
            cotizaciones[suc['id']] = {'compra': cambioEnSucursal.compra, 'venta': cambioEnSucursal.venta, 'timestamp': cambioEnSucursal.timestamp.strftime("%Y-%m-%d %H:%M:%S")}
        
        return { self.ident : cotizaciones }


    def test(self):
        cc = CambiosChaco()
        #sucursales
        suc = cc.getSucursales()
        #print(json.dumps(suc, indent=4))

        #cotizaciones
        coti = cc.getCotizaciones()
        #print(coti)
        print(json.dumps(coti, indent=4))
