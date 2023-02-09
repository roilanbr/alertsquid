# Alerta de acceso Squid Proxy
## Resumen
Este script leerá el archivo log que registra los accesos a páginas no permitidas, por ejemplo **xvideo.com**, **xnxx.com**, etc. Y luego enviará un mensaje de alerta por `Correo`, `wathsapp` o `Telegram`.

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

## Variables a modificar

 

| Variable    | Explicación                      |
|------------ | -------------------------------- |
| `log_file`  | Ruta al archivo `alertsquid.log` |
| `tmp_file`  | Ruta al archivo `tmp.log`        |
| `csv_file`  | Ruta al archivo `tmp.log`        |
| `countdown` | Tiempo de espera para comprobar  |

