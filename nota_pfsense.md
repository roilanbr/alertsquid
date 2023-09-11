# Configuracion especifica para PfSense

* Instalar el paquete `Shellcmd` por la interfaz web: `Sistema > |Gerente de empaquetación > |Paquetes disponibles`. En el cuadro de busqueda escribir shellcmd e instalar
* Luego ir a: `Servicios > |Shellcmd`, y le damos al botón `[añadir]` y poner lo siguiente.

```bash
      Command: usr/local/bin/python3.11 /opt/alertsquid/alertsquid.py
Shellcmd Type: shellcmd
  Descripción: Alerta por Telegram de navegacion a web prohibidas 
```

El script necesita el módulo `requests` para instalarlo ejecuta lo siguiente
> **`Nota:`**
> Recuerda cambiar *python3.11* por tu versión de python



```bash
# Para instalar pip y actualizar
python3.11 -m ensurepip
pip3 install --upgrade pip

# Instalar el modulo `requests` 
pip install requests
```

