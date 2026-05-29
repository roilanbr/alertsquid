# Alerta de acceso Squid Proxy
## Resumen

Este script leerá el archivo '.log' que registra los accesos a páginas no permitidas, por ejemplo **xvideo.com**, **xnxx.com**, etc. Y luego envía un mensaje de alerta por `Telegram`.

## Instalación

Copiar los archivos necesarios

```bash
cp -r src/alertsquid /opt/
```

## Configuracion de squid

Debe configurar `squid.conf` de la siguiente manera, crear una ACL de tipo `dstdomain` o `url_regex` en dependencia de lo  que quieras.

```bash
nano /etc/squid/squid.conf
# Luego ir a la sección `TAG: access_log` y agregar otra linea.
 
[...]
# acl alert_domain url_regex -i xvideo porn xnxx
acl alert_domain dstdomain -i xvideo.com xnxx.com

# Default (No modificar):
access_log daemon:/var/log/squid/access.log squid

# Nueva línea a crear
access_log daemon:/var/log/squid/alertsquid.log squid alert_domain
[...]
```

Luego ejecute lo siguiente:

```sh
# para comprobar la configuración
squid -k p

# para recargar la configuración
squid -k r

# para reiniciar squid
systemctl restart squid
```

## Variables a modificar en `alertsquid.py`

| Variable       | Explicación                      |
|--------------- | -------------------------------- |
| `log_file`     | Ruta al archivo `alertsquid.log`
| `url_analizer` | El URL del analizador de `lighsquid`
| `countdown`    | Tiempo de espera para comprobar
| `token`        | Toke de acceso a la API de Telegram
| `chat_id`      | ID del chat al que se envia el mensaje

## Autoiniciar
### **Para init**

Ejecutar lo siguiente:

```bash
# Copiar el script del servicio
cp /opt/alertsquid/service_init.sh /etc/init.d/alertsquid

# Enlace simbólico para que se inicie automaticamente
ln -s /etc/init.d/alertsquid /etc/rc.d/alertsquid

# Iniciar, parar, reiniciar, estado
service alertsquid start
service alertsquid stop
service alertsquid status

```

### **Para systemd**

Ejecutar lo siguiente:

```bash
# Copiar el script del servicio
cp service_systemd.service /etc/systemd/system/alertsquid.service

# Habilitar, iniciar y comprobar el estado
sudo systemctl enable alertsquid.service
sudo systemctl start alertsquid.service
sudo systemctl status alertsquid.service
```

### **Para PfSense**

Con el script `service_pfs.sh` se ejecutará `alertsquid.py` pero si ya está iniciado no lo ejecutará.

#### **Autoiniciar el script con `Shellcmd`**

> **`NOTA:`** No está bien probada esta configuración

* Instalar el paquete `Shellcmd` por la interfaz web: `[System] > [Package Manager] > [Paquetes disponibles]`. En el cuadro de busqueda escribir `shellcmd` e instalar
* Luego ir a: `[Servicios] > [Shellcmd]`, y le damos al botón `[añadir]` y poner lo siguiente.

<!-- 
┏━━━┳━━━┓
┃   ┃   ┃
┣━━━╋━━━┫
┃   ┃   ┃
┗━━━┻━━━┛
 -->
```bash
              ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
      Command ┃bash /opt/alertsquid/service_pfs.sh  ┃
              ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
              ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
Shellcmd Type ┃shellcmd                             ┃
              ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
              ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
  Description ┃Alerta de navegación a web prohibidas┃
              ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

#### **Autoiniciar el script con `cron`**

Con esto se lanza el script `/opt/alertsquid/service_pfs.sh` cada 5 minutos, si `alertsquid.py` esta ejecutandoce no se bolverá a ejecutar.

Por la interfaz web ir a: `[Servicios] > [Cron]`, y le damos al botón `[añadir]` y poner lo siguiente.


```bash
             ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
      Minute ┃*/5                                   ┃
             ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
             ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        Hour ┃*                                     ┃
             ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
  Day of the ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
       Month ┃*                                     ┃
             ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
Month of the ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        Year ┃*                                     ┃
             ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
  Day of the ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        Week ┃*                                     ┃
             ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
             ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        User ┃root                                  ┃
             ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
             ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
     Command ┃bash /opt/alertsquid/service_pfs.sh   ┃
             ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```
