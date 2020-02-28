import json
from datetime import datetime
from providers.cambioschaco import Cambioschaco
from providers.vision import Vision
from providers.interfisa import Interfisa
from providers.alberdi import Alberdi


def mergeAllQuotes():
    cambios = {}

    cc = Cambioschaco()
    ccc = cc.getCotizaciones()
    cambios.update(ccc)

    v = Vision()
    cv = v.getCotizaciones()
    cambios.update(cv)

    ib = Interfisa()
    ibc = ib.getCotizaciones()
    cambios.update(ibc)

    alb = Alberdi()
    albc = alb.getCotizaciones()
    cambios.update(albc)

    return cambios
    
if __name__ == "__main__":
    cambios = mergeAllQuotes()
    print(json.dumps(cambios, indent=4))
