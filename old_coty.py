#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
import requests
import urllib3

from decimal import Decimal
from bs4 import BeautifulSoup
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

## Format
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def format_decimal(number):
    return str(number).replace(".", "").replace(",", ".")


### extraccion de bancos y financieras


def maxi():
    today = datetime.today().strftime("%d%m%Y")
    url = "https://www.maxicambios.com.py/"
    try:
        soup = BeautifulSoup(
            requests.get(
                url,
                timeout=10,
                headers={"user-agent": "Mozilla/5.0"},
                verify=False,
            ).text,
            "html.parser",
        )

        tr_dolar = soup.find(class_="fixed-plugin").find("table").find("tbody").find("tr")

        compra = tr_dolar.find_all('td')[1].text
        venta  = tr_dolar.find_all('td')[2].text

    except requests.ConnectionError:
        compra, venta = 0, 0
    except:
        compra, venta = 0, 0

    return Decimal(compra), Decimal(venta)


def bcp():
    try:
        soup = BeautifulSoup(
            requests.get(
                "https://www.bcp.gov.py/webapps/web/cotizacion/monedas",
                timeout=10,
                headers={"user-agent": "Mozilla/5.0"},
                verify=False,
            ).text,
            "html.parser",
        )
        ref = soup.select("#cotizacion-interbancaria > tbody > tr > td:nth-of-type(4)")[
            0
        ].get_text()
        ref = ref.replace(".", "").replace(",", ".")
        soup = BeautifulSoup(
            requests.get(
                "https://www.bcp.gov.py/webapps/web/cotizacion/referencial-fluctuante",
                timeout=10,
                headers={"user-agent": "Mozilla/5.0"},
                verify=False,
            ).text,
            "html.parser",
        )
        compra_array = soup.find(
            class_="table table-striped table-bordered table-condensed"
        ).select("tr > td:nth-of-type(4)")
        venta_array = soup.find(
            class_="table table-striped table-bordered table-condensed"
        ).select("tr > td:nth-of-type(5)")
        posicion = len(compra_array) - 1
        compra = compra_array[posicion].get_text().replace(".", "").replace(",", ".")
        venta = venta_array[posicion].get_text().replace(".", "").replace(",", ".")
    except requests.ConnectionError:
        compra, venta, ref = 0, 0, 0
    except:
        compra, venta, ref = 0, 0, 0

    return Decimal(compra), Decimal(venta), Decimal(ref)


def setgov():
    try:
        soup = BeautifulSoup(
            requests.get("http://www.set.gov.py/portal/PARAGUAY-SET", timeout=10).text,
            "html.parser",
        )
        compra = (
            soup.select("td.UICotizacion")[0].text.replace("G. ", "").replace(".", "")
        )
        venta = (
            soup.select("td.UICotizacion")[1].text.replace("G. ", "").replace(".", "")
        )
    except requests.ConnectionError:
        compra, venta = 0, 0
    except:
        compra, venta = 0, 0

    return Decimal(compra), Decimal(venta)


def amambay():
    try:
        soup = requests.get(
            "http://www.bancoamambay.com.py/ebanking_ext/api/data/currency_exchange",
            timeout=10,
        ).json()
        compra = soup["currencyExchanges"][0]["purchasePrice"]
        venta = soup["currencyExchanges"][0]["salePrice"]
    except requests.ConnectionError:
        compra, venta = 0, 0
    except:
        compra, venta = 0, 0

    return Decimal(compra), Decimal(venta)


def eurocambio():
    try:
        url = "https://eurocambios.com.py/v2/sgi/utilsDto.php"
        data = {"param": "getCotizacionesbySucursal", "sucursal": "1"}
        result = requests.post(url, data, timeout=10).json()
        compra = result[0]["compra"]
        venta = result[0]["venta"]
    except requests.ConnectionError:
        compra, venta = 0, 0
    except:
        compra, venta = 0, 0

    return Decimal(compra), Decimal(venta)


def myd():
    try:
        soup = BeautifulSoup(
            requests.get("https://www.mydcambios.com.py/", timeout=10).text,
            "html.parser",
        )
        compra = soup.select(
            "div.cambios-banner-text.scrollbox > ul:nth-of-type(2) > li:nth-of-type(2) "
        )[0].text
        venta = soup.select(
            "div.cambios-banner-text.scrollbox > ul:nth-of-type(2) > li:nth-of-type(3) "
        )[0].text
    except requests.ConnectionError:
        compra, venta = 0, 0
    except:
        compra, venta = 0, 0

    return Decimal(compra), Decimal(venta)


# def familiar():  # Comentado porque el servidor bloquea las peticiones
#     try:
#         soup = BeautifulSoup(
#             requests.get('https://www.familiar.com.py/', timeout=10).text, "html.parser")
#         compra = soup.select(
#             'hgroup:nth-of-type(1) > div:nth-of-type(2) > p:nth-of-type(2)')[0].get_text().replace('.', '')
#         venta = soup.select(
#             'hgroup:nth-of-type(1) > div:nth-of-type(3) > p:nth-of-type(2)')[0].get_text().replace('.', '')
#     except requests.ConnectionError:
#         compra, venta = 0, 0
#     except:
#         compra, venta = 0, 0

#     return Decimal(compra), Decimal(venta)


def bbva():
    try:
        soup = requests.get(
            "https://www.bbva.com.py/Yaguarete/public/quotations", timeout=10
        ).json()
        compra = soup[0]["cashBuyPrice"]
        venta = soup[0]["cashSellPrice"]
    except requests.ConnectionError:
        compra, venta = 0, 0
    except:
        compra, venta = 0, 0

    return Decimal(compra), Decimal(venta)


def mundial():
    try:
        url = "http://www.mundialcambios.com.py/json.php"
        data = {"id": "6"}
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "es-ES,es;q=0.9",
            "Connection": "keep-alive",
            "Content-Length": "4",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
        }
        result = requests.post(url, data, headers=headers, timeout=10).json()
        compra = result["data"]["cambios"]["0"]["cot_compra"]
        venta = result["data"]["cambios"]["0"]["cot_venta"]
    except requests.ConnectionError:
        compra, venta = 0, 0
    except:
        compra, venta = 0, 0

    return Decimal(compra), Decimal(venta)

############ creacion del JSON final (no modular)

def create_json():
    mcompra, mventa = maxi()
    bcpcompra, bcpventa, bcpref = bcp()
    setcompra, setventa = setgov()
    ambcompra, ambventa = amambay()
    eccompra, ecventa = eurocambio()
    mydcompra, mydventa = myd()
    bbvacompra, bbvaventa = bbva()
    # famicompra, famiventa = familiar()
    wcompra, wventa = mundial()

    respjson = {
        "dolarpy": {
            "maxicambios": {"compra": mcompra, "venta": mventa},
            "bcp": {
                "compra": bcpcompra,
                "venta": bcpventa,
                "referencial_diario": bcpref,
            },
            "set": {"compra": setcompra, "venta": setventa},
            "amambay": {"compra": ambcompra, "venta": ambventa},
            "mydcambios": {"compra": mydcompra, "venta": mydventa},
            "eurocambios": {"compra": eccompra, "venta": ecventa},
            # 'familiar': {
            #     'compra': famicompra,
            #     'venta': famiventa
            # }
            "bbva": {"compra": bbvacompra, "venta": bbvaventa},
            "mundialcambios": {"compra": wcompra, "venta": wventa},
        },
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    return json.dumps(
        respjson,
        indent=4,
        sort_keys=True,
        separators=(",", ": "),
        default=decimal_default,
    )

### leer JSON
def get_output():
    with open("dolar.json", "r") as f:
        response = f.read()
    return response

### escribir JSON (llama a todo lo demás del archivo)
def write_output():
    response = create_json()
    with open("dolar.json", "w") as f:
        f.write(response)

def json_format():
    #variables para usar de demo abajo
    compra = 0
    venta = 0
    timestamp = 0

    json_old = {
        "dolarpy": {
                "cambiosalberdi": {"compra": compra, "venta": venta},
                "cambioschaco": {"compra": compra, "venta": venta},
                "maxicambios": {"compra": compra, "venta": venta},
                "bcp": {
                    "compra": compra,
                    "venta": venta,
                    "referencial_diario": venta, #bcpref,
                },
                "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                #...
            }
    }

    json_new = {
        "dolarcde": {
            "cambioschaco": {
                "km4": {"compra": compra, "venta": venta, "timestamp": timestamp},
                "shopping-jardin": {"compra": compra, "venta": venta, "timestamp": timestamp},
                "shopping-del-este": {"compra": compra, "venta": venta, "timestamp": timestamp},
                "resumen": {"maxcompra": "km4", "minventa": "shopping-jardin"},
            },
            "bonanza": {
                "matriz": {"compra": compra, "venta": venta, "timestamp": timestamp},
                "saba": {"compra": compra, "venta": venta, "timestamp": timestamp},
                "resumen": {"maxcompra": "matriz", "minventa": "matriz"},
            },
            "resumen": {
                "maxcompra": "cambioschaco-km4", "minventa": "bonanza-saba",
            }
        }
    }

    ubicaciones_json = {    #cada proveedor debe proveer una lista de nombres de sucursales y sus ubicaciones
        "cambioschaco": {
            "sucursales": [ 
                { "id1": "km4", "direccion": "Avda. Tal Cosa", "ubicacion": "Lat-Long" },
                { "id2": "shopping-jardin", "direccion": "Avda. Tal Cosa", "ubicacion": "Lat-Long"},
            ]
        }
    }

write_output()
