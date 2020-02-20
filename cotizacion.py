from datetime import datetime
from providers.cambioschaco import CambiosChaco

class Cotizacion():
    def __init__(self, compra, venta):
        self.compra = compra
        self.venta = venta
        self.timestamp = datetime.now()

if __name__ == "__main__":
    cotiz = Cotizacion(100, 200)
    print(f"Cotización: compra = {cotiz.compra}, venta = {cotiz.venta}. Fecha: {cotiz.timestamp}")

    cc = CambiosChaco()
    suc = cc.getSucursales()
    print(type(suc))
    print(suc)
