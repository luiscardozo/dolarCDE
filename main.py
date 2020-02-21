import json
from datetime import datetime
from providers.cambioschaco import CambiosChaco
from providers.vision import Vision
from providers.interfisa import Interfisa


def mergeAllQuotes():
    cambios = {}

    cc = CambiosChaco()
    ccc = cc.getCotizaciones()
    cambios.update(ccc)

    v = Vision()
    cv = v.getCotizaciones()
    cambios.update(cv)

    ib = Interfisa()
    ibc = ib.getCotizaciones()
    cambios.update(ibc)

    return cambios
    
if __name__ == "__main__":
    cambios = mergeAllQuotes()
    print(json.dumps(cambios, indent=4))
