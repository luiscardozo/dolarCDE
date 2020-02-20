from datetime import datetime

class Cotizacion():
    def __init__(self, compra, venta):
        self.compra = compra
        self.venta = venta
        self.timestamp = datetime.now()

    def __str__(self):
        return f"compra: {self.compra}, venta: {self.venta} ({self.timestamp})"

    def getValuesDict(self):
        return {'compra': self.compra, 'venta': self.venta,
                'timestamp': self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
