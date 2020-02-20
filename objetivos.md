Objetivos de DolarCDE
1. Que sea modular: que se pueda extender alguna interfaz y agregar nuevos proveedores rápidamente
    
    Intentar que los módulos base implementen las llamadas necesarias básicas y que los demás módulos sólo pasen datos necesarios (ej. URL, regex/xpath, etc)

    Una llamada puede retornar:
    * JSON (ej.: Cambios Chaco, Alberdi, Interfisa, Amambay, Eurocambio, BBVA, Mundial)
    * HTML (ej.: Visión Banco, Maxicambios, BCP, SET, MyD, Familiar (bloqueado))
    * 

2. Conocer la mejor cotización en cada momento
3. No mostrar (o mostrar en rojo) las cotizaciones que no pudieron ser actualizadas
