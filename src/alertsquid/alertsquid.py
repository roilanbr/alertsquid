import os           # Misceláneas del sistema operativo
import sys
import tomllib      # Procesar archivos .toml
import time         # Manejo a fecha, hora y conversiones
from ipaddress import ip_address, ip_network    # Manejo de direcciones IP
import urllib.request
import urllib.parse

os.system("clear")  # Limpiar la consola

# COLORS AND TAG
CR = "\033[91m"; CG = "\033[92m"; CY = "\033[93m"; CB = "\033[94m"; CC = "\033[96m"; NC = "\033[0m"
OK    = f"[{CG} OK    {NC}]"
ERROR = f"[{CR} ERROR {NC}]"
WARN  = f"[{CY} WARN  {NC}]"
INFO  = f"[{CB} INFO  {NC}]"
SEND  = f"[{CB} SEND  {NC}]"
DEBUG = f"[{CY} DEBUG {NC}]"


#################################################
#                   CLASS
#################################################
class Module():
    # Comprobar si existe un archivo
    def check_file_exist(path_file):
        if not os.path.isfile(path_file):
            print(f"{ERROR} File {CY}{path_file}{NC} not found.\n")
            exit()

    # Mostrar decimal
    def decimal(number, decimals=2):
        factor = 10 ** decimals
        return int(number * factor) / factor

    # Mostrar Bytes en base 1000 (Bi, KiB, MiB, GiB, TiB) | 1024 (B, KB, MB, GB, TB)
    def parse_bytes(bytes, base=1024):
        if base == 1000: um = "K"
        if base == 1024: um = "Ki" 
        
        # Solo para Squid Proxy que usa KB base 1024 según documentación, comentar para lo demas
        if base == 1024: um = "K"

        if bytes < base:
            return f"{bytes}_B"
        elif bytes < 1 * (base ** 2):
            return f"{Module.decimal((bytes / base))}_{um}B"
        elif bytes < 1 * (base ** 3):
            return f"{Module.decimal((bytes / base ** 2))}_{um}B"
        elif bytes < 1 * (base ** 4):
            return f"{Module.decimal((bytes / base ** 3))}_{um}B"
        elif bytes >= 1 * (base ** 4):
            return f"{Module.decimal((bytes / base ** 4))}_{um}B"

    # Contar la lineas que tiene un archivo de texto
    def count_lines(file):
        with open(file) as file:
            lines = 0
            for line in file: # Bucle para contar las lineas que tiene el archivo
                lines += 1    # Ir sumando los registros
        return lines


#################################################
#                  ARGUMENT
#################################################

def show_verbose(message, state = False):
    if state:
        print(message)

msg_help = f""" 
Ayuda de Alertsquid
=================================================
{CG}-h, --help{NC}    Mostrar esta ayuda
{CG}-v, --verbose{NC} Mostar detalles
"""
# Lista de argumentos
argv_list = ['-h', '--help', '-v', '--verbose']

argv_passed    = sys.argv[1:]
argv_help    = False
argv_verbose = False

if len(argv_passed) > 0:
    for argv in  argv_passed:
        if argv in ("-h", "--help")   : argv_help    = True # Ayuda
        if argv in ("-v" "--verbose") : argv_verbose = True # Detalles

    # Comprobar si es un argumento es correcto
    if not argv in argv_list:
        print(f"{ERROR} El argumento {CG}{argv}{NC} no es válido, pase {CG}-h{NC} para mostrar la ayuda.")
        exit()

    # Mostrar los argumentos
    if argv_verbose:
        # print(f"{DEBUG} Argumentos: {argv_list[1:]}")
        show_verbose(f"{DEBUG} Argumentos: {argv_passed[:]}", argv_verbose)

    # Mostrar la ayuda
    if argv_help:
        print(msg_help); exit()


#################################################
#                   VARIABLES
#################################################

# ¡¡¡¡¡ NO MODIFICAR !!!!!
base_dir     = os.path.dirname(__file__) # Directorio de trabajo
file_conf    = f"{base_dir}/alertsquid.conf"
file_ip2name = f"{base_dir}/ip2name.conf"
file_ip2ignore = f"{base_dir}/ip2ignore.conf"
file_outbox = f"{base_dir}/outbox.db"

config_text = '''
# CONFIGURACIÓN GLOBAL
[global]

# Ruta al archivo "alertsquid.log"
log_file = "/var/log/squid/alertsquid.log"
url_analizer = "http://lighsquid.tudominio.com"

# Tiempo de espera en segundos antes de chequear los log
countdown = 5

# DATOS PARA TELEGRAM
[telegram]

# Token para acceder a la API HTTP
token = "tu_token_para_la_api_de_telegram"

# Bot chat id
chat_id = chat_id_donde_enviar_mensaje
'''
ip2name_text = '# Clientes sala A  \nPC1 192.168.0.21 \nPC2 192.168.0.22'
ip2ignore_text = f'192.168.0.21 \t# Ignorar host \n192.168.50.0/24 # Ignorar red'

# Crear archivos de configuración si no existen
if not os.path.exists(file_conf)     :
    with open(file_conf, "w", encoding='utf-8') as f: f.write(config_text)
if not os.path.exists(file_ip2name)  :
    with open(file_outbox, "w", encoding='utf-8') as f: f.write(ip2name_text)
if not os.path.exists(file_ip2ignore):
    with open(file_outbox, "w", encoding='utf-8') as f: f.write(ip2ignore_text)
exit()
# Cargar variables del archivo de configuración
Module.check_file_exist(file_conf)
with open(file_conf, "rb") as f:
    load_config = tomllib.load(f)

file_log      = load_config.get("global", {}).get("log_file")
url_analizer  = load_config.get("global", {}).get("url_analizer")
countdown     = load_config.get("global", {}).get("countdown")
token         = load_config.get("telegram", {}).get("token")
chat_id       = load_config.get("telegram", {}).get("chat_id")
url_telegram  = f"https://api.telegram.org/bot{token}/sendMessage"


#################################################
#                   FUNCTIONS
#################################################

# Funcion para cargar archivo en una lista db
def f_load_db(file):
    db = []
    with open(file, "r", encoding='utf-8') as f:
        lines = f.readlines() 
        for item in lines:
            # Eliminar los espacios al inicio | final, y saltar líneas vacías o comentarios
            item = item.strip()
            if not item or item.startswith("#"):
                continue
            db.append(item)
        return db


def main():
    # Guardar timestamp de 'alertsquid.log'
    Module.check_file_exist(file_log)
    exit()
    timestamp_file_log_old = int(os.path.getctime(file_log)) # Timestamp old

    # Guardar en variable los registros inicial que tiene "alertsquid.log"
    record_old = Module.count_lines(file_log)
    show_verbose(f"{DEBUG} Log antiguos: {record_old}", argv_verbose)
    # print(argv_verbose)
   
    # ===============================================
    #                   CARGA DE DATOS
    # ===============================================
    Module.check_file_exist(file_ip2name)
    Module.check_file_exist(file_ip2ignore)
    db_ip2name = f_load_db(file_ip2name)
    db_ip2ignore = f_load_db(file_ip2ignore)

    # ===============================================
    #                      BUCLE
    # ===============================================
    while True:
        timestamp_file_log_current = int(os.path.getctime(file_log)) # Timestamp actual

        # Comparar fechas de alersquid.log y actualizado la variable 'record_old'
        if timestamp_file_log_old < timestamp_file_log_current:
            show_verbose(f"{INFO} {CY}{file_log}{NC} ACTUALIZADO", argv_verbose)
            record_old = record_total

        # Calcular las nuevas lineas desde la última vez que se comprobó
        record_total = Module.count_lines(file_log)
        record_diff = record_total - record_old
        show_verbose(f"{DEBUG} Total de registros: {record_total}", argv_verbose)
        print(f"{INFO} Registros nuevos: {record_diff}")

 
        # ------------------------------------------
        # ENVIAR MENSAJE DE 'inbox.db' A TELEGRAM
        # ------------------------------------------

        # Si NO HAY nuevos registros (<= 0 ) y si existe el archivo outbox.db
        if record_diff <= 0:
            if os.path.exists(file_outbox):
                with open(file_outbox, "r", encoding='utf-8') as f:
                    all_message_outbox = f.read()
                    head_message  = "🚨 Alerta https://urlscan.io/domain/dominio_a_buscar"
                    legend_message = "🟢 ALLOW | 🟡 ABORT | 🔴 DENY"
                    message_format =  f"{head_message} \n{all_message_outbox}"
                    message_ok = message_format.strip()
                    
                    print(f"{SEND} Enviando Mensaje de {CY}{file_outbox}{NC} a Telegram")
                    headers = {'Content-Type': 'application/json'}
                    data = urllib.parse.urlencode({'chat_id': f"-100{chat_id}", 'text': message_ok, "parse_mode": "HTML"}).encode()

                    # Enviar el mensaje de 'outbox.db' manejando los errores
                    try:
                        # url_telegram = f"https://api.telegram.org/bot{token}/sendMessageeeee"
                        show_verbose(f"{all_message_outbox}\n", argv_verbose)
                        urllib.request.urlopen(url_telegram, data=data)
                        
                        # Eliminar el archivo 'outbox.db' si existe
                        if os.path.exists(file_outbox): os.remove(file_outbox)
                        show_verbose(f"{DEBUG} Eliminando archivo {file_outbox}")

                    except urllib.error.URLError as e:
                        # Mostar el error y guardar mensage en el archivo 'ouxbox.db'
                        print(f"{ERROR} {e}")
                        continue


        # Descomentar para probar
        # record_diff = 1

        # Si HAY nuevos registros (> 0)
        if record_diff > 0:
            # ------------------------------------------
            # PROCESAR LOS NUEVOS REGISTROS
            # ------------------------------------------
            all_message = ""
            Module.check_file_exist(file_log)
            with open(file_log, "r", encoding="utf-8") as f:
                record_list = f.readlines()[-record_diff:] # Coger los ultimos registros
                print(f"{INFO} Procesando registros")
                # all_message = ""
                no_record_format = 0
                for item in record_list:

                    # print(f"0 timestamp    : {item.split()[0]}")
                    # print(f"2 client_ip_log: {item.split()[2]}")
                    # print(f"3 status       : {item.split()[3]}")
                    # print(f"4 bytes        : {item.split()[4]}")
                    # print(f"6 url_dst: {item.split()[6]}")
                    # exit()

                    # ...............................................
                    # Formatear timestamp
                    # ...............................................
                    timestamp = float(item.split()[0])
                    timestamp = time.gmtime(int(timestamp))		           # Convertir en una estructura de tiempo
                    timestamp = time.strftime('%Y/%m/%d %H:%M', timestamp) # Formatear fecha
                    date  = timestamp.split()[0]
                    year  = date.split("/")[0]
                    month = date.split("/")[1]
                    day   = date.split("/")[2]

                    # ...............................................
                    # Formatear IP del cliente
                    # ...............................................
                    client_ip_log = item.split()[2]
                    
                    # Ignorar IP si está en el archivo ip2ignore.conf
                    ignore = None
                    for ip_red in db_ip2ignore:
                        ip_red = ip_red.split()[0]

                        # Comprobar si 'ip_red' es una IP o una RED
                        try:
                            ip_address(ip_red)
                            if ip_address(ip_red) == ip_address(client_ip_log):
                                print(f"{WARN} Ignorando IP : {client_ip_log}")
                                ignore = True
                        # Si 'try' da error se considera que es una RED
                        except ValueError:
                            if ip_address(client_ip_log) in ip_network(ip_red):
                                print(f"{WARN} Ignorando Red: {ip_red}")
                                ignore = True
                    if ignore == True: continue

                    # Formatear IP
                    for record in db_ip2name:
                        client_name_ip2name = record.split()[0]
                        client_red_ip2name = record.split()[1]
                        
                        # Comparar IP del cliente esta el la RED  usando 'db_ip2name' y formatear
                        if ip_address(client_ip_log) in ip_network(client_red_ip2name):
                            ip_format = f"{client_ip_log} ( {client_name_ip2name} )"
                        else:
                            ip_format = client_ip_log

                    # ...............................................
                    # Formatear status
                    # ...............................................
                    status = item.split()[3]
                    status = status.split("/")[0]
                    if status == "TCP_MISS" or status == "TCP_TUNNEL": status = "🟢"
                    if status == "TCP_MISS_ABORTED": status = "🟡"
                    if status == "TCP_DENIED": status = "🔴"
                    
                    # ...............................................
                    # Formatear los bytes descargado
                    # ...............................................
                    size_bytes = item.split()[4]
                    size_bytes = Module.parse_bytes(int(size_bytes))

                    # ...............................................
                    # No formatear
                    # ...............................................
                    url_dst = item.split()[6]

                    # Construir mensage para telegram
                    href = f"{url_analizer}/day_detail.cgi?year={year}&month={month}&day={day}"
                    message_parse = f"{status} {timestamp} <a href='{href}'>{ip_format}</a> {size_bytes} 🌐<code>{url_dst}</code>"
                    all_message = all_message + f"\n{message_parse}"
                    no_record_format += 1
                
                # Saltar si los registros son <= 0 
                show_verbose(f"{DEBUG} No. registros formateado: {no_record_format}", argv_verbose)
                if no_record_format <= 0: time.sleep(countdown); continue
                no_record_format = 0 # Restablecer valor

                # Cargar mensages del archivo 'outbox.db si existe'
                all_message_outbox = ""
                if os.path.exists(file_outbox):
                    with open(file_outbox, "r", encoding='utf-8') as f:
                        all_message_outbox = f.read()

                # Agregar cabecera al mensaje
                head_message  = "🚨 Alerta https://urlscan.io/domain/dominio_a_buscar"
                legend_message = "🟢 ALLOW | 🟡 ABORT | 🔴 DENY"
                message_format =  f"{head_message} \n{legend_message} \n{all_message_outbox} {all_message}"
            message_ok = message_format.strip()

            # ------------------------------------------
            # ENVIAR MENSAJE A 'TELEGRAM
            # ------------------------------------------
            print(f"{SEND} Enviando Mensaje a Telegram")
            headers = {'Content-Type': 'application/json'}
            data = urllib.parse.urlencode({'chat_id': f"-100{chat_id}", 'text': message_ok, "parse_mode": "HTML"}).encode()

            # Enviar el mensaje manejando los errores
            try:
                # url_telegram = f"https://api.telegram.org/bot{token}/sendMessageeeee"
                show_verbose(f"{DEBUG} Mensages a enviar:", argv_verbose)
                all_message = f"{all_message_outbox} {all_message}"
                show_verbose(f"\n{all_message.strip()}\n", argv_verbose)
                urllib.request.urlopen(url_telegram, data=data)
                
                # Eliminar el archivo 'outbox.db' si existe
                if os.path.exists(file_outbox): os.remove(file_outbox)
                show_verbose(f"{DEBUG} Eliminando archivo {file_outbox}")

            except urllib.error.URLError as e:
                # Mostar el error y guardar mensage en el archivo 'ouxbox.db'
                print(f"{ERROR} {e}")
                print(f"{INFO} Guardando el mensage en el archivo {CY}{file_outbox}{NC})")
                # all_message = f"{all_message_outbox} {all_message}"
                all_message = f"{all_message}"
                with open(file_outbox, 'w') as f: f.write(f"{all_message}")



            # Reestablecer los registro a 0
            show_verbose(f"{DEBUG} Reestablecer registros a 0", argv_verbose)
            record_old = record_total
            show_verbose(f"{DEBUG} Actualizar timestamp del archivo {CY}{file_log}{NC}", argv_verbose)
            timestamp_file_log_old = timestamp_file_log_current
            # exit()
        time.sleep(countdown)

if __name__ == "__main__":
    # Manejar interruccion del usuario 'Ctr+C'
    try:
        main()
    except KeyboardInterrupt:
        # Limpiar recursos si es necesario. Cerrar archivos, conexiones a BD, etc.
        print(f"\r{WARN} Programa interrumpido por el usuario")
        sys.exit(0)