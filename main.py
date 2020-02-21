import json
from datetime import datetime
from providers.cambioschaco import CambiosChaco
from providers.vision import Vision

if __name__ == "__main__":
    
    cambios = {}

    cc = CambiosChaco()
    ccc = cc.getCotizaciones()

    cambios.update(ccc)


    v = Vision()
    cv = v.getCotizaciones()
    cambios.update(cv)

    print(json.dumps(cambios, indent=4))
    