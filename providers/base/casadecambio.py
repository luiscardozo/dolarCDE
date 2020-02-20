from datetime import datetime
from abc import ABC, abstractmethod

class CasaDeCambio(ABC):

    @abstractmethod
    def getSucursales(self):    #si, a veces mezclo inglés con español
        pass

    @abstractmethod
    def getCotizaciones(self):
        pass

### ejemplos:

    #def listarSucursales(self):
        # return { "casadecambio":
        #     { "sucursales": [
        #         { "id1": "km4", "direccion": "Avda. Tal Cosa", "ubicacion": "Lat-Long" },
        #         { "id2": "km10", "direccion": "Avda. Tal Cosa", "ubicacion": "Lat-Long" },
        #         { "id3": "km20", "direccion": "Avda. Tal Cosa", "ubicacion": "Lat-Long" },
        #     ]
        #     }
        # }

    # def obtenerConexionInfo(self):
    #     """Esto también debería ser algo interno."""
    #     return { "url": "http://dolar.luisc.me", "headers": "", "data": "", "type": "JSON/HTML" }

    # def obtenerCambiosInfo(self):
    #     """
    #     Cómo debe hacer el controlador para obtener los datos de compra o venta?
    #     --->>> MEJOR: debe estar encapsulado en cada implementación y retornar sólo las cotizaciones
    #     """
    #     return { 
    #         "moneda": "usd",
    #         "compra": "div.cambios-banner-text.scrollbox > ul:nth-of-type(2) > li:nth-of-type(2) ",
    #         "venta":  "div.cambios-banner-text.scrollbox > ul:nth-of-type(2) > li:nth-of-type(1) ",
    #         "type": "XPATH" }

    # def obtenerCotizacion(self):
    #     compra = 0
    #     venta = 0
    #     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     return {
    #         "casadecambio": {
    #             "km4": {"compra": compra, "venta": venta, "timestamp": timestamp},
    #             "shopping-jardin": {"compra": compra, "venta": venta, "timestamp": timestamp},
    #             "shopping-del-este": {"compra": compra, "venta": venta, "timestamp": timestamp},
    #             "resumen": {"maxcompra": "km4", "minventa": "shopping-jardin"},
    #         }
    #     }

# if __name__ == "__main__":
#     cdc = CasaDeCambio()
#     suc = cdc.listarSucursales()
#     type(suc)
#     print(suc)
#     cot = cdc.obtenerCotizacion()
#     type(cot)
#     print(cot)