# Alerta de acceso Squid Proxy
## Resumen
Este script leerá el archivo log que registra los accesos a páginas no permitidas, por ejemplo **xvideo.com**, **xnxx.com**, etc. Y luego enviará un mensaje de alerta por `Correo` o `Telegram`.

## Instalación

El script necesita el módulo `requests` para instalarlo ejecuta lo siguiente

```bash
# Para instalar pip y actualizar
python -m ensurepip
pip install --upgrade pip

# Instalar el modulo `requests` 
pip install requests
```
Copia de archivos necesarios

```bash
mkdir -p /opt/alertsquid
cp alertsquid.py /opt/alertsquid/
```


## Configuracion de squid

Debe configurar `squid.conf` de la siguiente manera, crear una ACL de tipo `dstdomain` o `url_regex` en dependencia de lo  que quieras.

Luego ir a la sección `TAG: access_log` y agregar otra linea.

    nano /etc/squid/squid.conf


```sh 
[...]
# acl alert_domain url_regex -i xvideo porn xnxx
acl alert_domain dstdomain -i xvideo.com xnxx.com

# Default:
access_log daemon:/var/log/squid/access.log squid
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

| Variable    | Explicación                      |
|------------ | -------------------------------- |
| `log_file`  | Ruta al archivo `alertsquid.log` |
| `tmp_file`  | Ruta al archivo `tmp.log`        |
| `csv_file`  | Ruta al archivo `csv.log`        |
| `countdown` | Tiempo de espera para comprobar  |

## Autoiniciar el script
### Para init

Ejecutar lo siguiente:

```bash
# Copiar el script del servicio
cp service_init.sh /etc/init.d/alertsquid

# Iniciar y comprobar el estado
service alertsquid start
service alertsquid status

# Enlace simbólico para que se inicie automaticamente
ln -s /etc/init.d/alertsquid /etc/rc.d/alertsquid
```
### Para systemd

Ejecutar lo siguiente:

```bash
# Copiar el script del servicio
cp service_systemd.service /etc/systemd/system/alertsquid.service

# Habilitar, iniciar y comprobar el estado
sudo systemctl enable alertsquid.service
sudo systemctl start alertsquid.service
sudo systemctl status alertsquid.service
```

### Para PfSense
Con el script `service_pfs.sh` se ejecutará `alertsquid.py` pero si ya está iniciado no lo ejecutará.
#### Autoiniciar el script con `Shellcmd`

> **`NOTA:`** No esta bien probada esta configuracion

* Instalar el paquete `Shellcmd` por la interfaz web: `System > |Package MManager > |Paquetes disponibles`. En el cuadro de busqueda escribir shellcmd e instalar
* Luego ir a: `Servicios > |Shellcmd`, y le damos al botón `[añadir]` y poner lo siguiente.

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
Shellcmd Type ┃shelcmd                              ┃
              ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
              ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
  Description ┃Alerta de navegación a web prohibidas┃
              ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```


#### Autoiniciar el script con `cron` cada 5 minutos


Por la interfaz web ir a: `Servicios > |Cron`, y le damos al botón `[añadir]` y poner lo siguiente.


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
