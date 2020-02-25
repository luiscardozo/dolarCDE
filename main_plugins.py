import json
from datetime import datetime
from providers.base.casadecambio import CasaDeCambio

import importlib
import pkgutil

import providers

def iter_namespace(ns_pkg):
    # Specifying the second argument (prefix) to iter_modules makes the
    # returned name an absolute name instead of a relative one. This allows
    # import_module to work without having to do additional modification to
    # the name.
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

def discoverPlugins():
    discovered_plugins = {
        name: importlib.import_module(name)
        for finder, name, ispkg
        in iter_namespace(providers)
    }

    return discovered_plugins


def mergeAllQuotes():
    cambios = {}

    plugins = discoverPlugins()

    for key, _module in plugins.items():
        
        if(key == 'providers.base'):
            continue

        casaDeCambioClass = getattr(_module, key.split('.')[1].title() )
        
        casaDeCambioInstance = casaDeCambioClass()
        #sucursales = casaDeCambioInstance.getSucursales()
        #print(sucursales)

        cotiz = casaDeCambioInstance.getCotizaciones()
        cambios.update(cotiz)

    return cambios
    
if __name__ == "__main__":
    cambios = mergeAllQuotes()
    print(json.dumps(cambios, indent=4))
