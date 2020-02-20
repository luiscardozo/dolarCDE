import string
import sys, os
import json
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from lib.casadecambio import CasaDeCambio
from lib.origintype import OriginType

class CambiosChaco(CasaDeCambio):

    idn = "cambioschaco"
    name = "Cambios Chaco"
    originType = OriginType.JSON
    urlTemplate = string.Template("https://www.cambioschaco.com.py/api/branch_office/${branch}/exchange")
    # luego: template_text.safe_substitute(branch=branchID))
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
            self.idn : { "sucursales": self.sucursales }
        }
        
    def getCotizaciones(self):
        pass


if __name__ == '__main__':
    cc = CambiosChaco()
    suc = cc.getSucursales()
    print(type(suc))
    print(suc)
    print("\n")
    print(json.dumps(suc, indent=4))