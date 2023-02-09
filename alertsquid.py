#! /usr/bin/python
# -*- coding: utf-8 -*-

# ======================================================
# IMPORTAR MODULOS
# ======================================================


# from os import path
import os; os.system("clear")


import logging as log                             # Level = DEBUG, INFO, WARNING, ERROR, CRITICAL
log.basicConfig(level=log.DEBUG, 
                    format="%(asctime)s - %(levelname)s - %(message)s",)
                    # filename="debug.log",
                    # filemode="a")

import time

# ======================================================
# VARIABLES
# ======================================================

base_dir = os.path.dirname(__file__)    # Directorio de trabajo
log_file = "logs/alertsquid.log"      # Ruta al archivo "alertsquid.log"
tmp_file = ".tmp/alert.log"            # Ruta al archivo "tmp.log"
csv_file = ".tmp/alert.csv"            # Ruta al archivo "tmp.log"
countdown = 5                           # Cuenta atrás

log.info("Varibles creadas")

# print(f"\n{base_dir} \n{log_file} \n{tmp_file} \n{csv_file} \n{countdown}\n")


# ======================================================
# FUNCIONES
# ======================================================

# Función para contar la lineas que tiene un archivo de texto
# Uso: fun_record(file)
def fun_count_lines(file):
    with open(file) as file:
        lines = 0

        for line in file:   # Bucle para contar las lineas que tiene el archivo
            lines += 1      # Ir sumando los registros
    return lines

# Función para calcular la difererncia entre 2 números
# Uso: fun_diff(num1, num2)
def fun_diff_num(num1, num2):
    diff = num1 - num2
    return diff

# Función para mostrar las últimas lineas espesificada de un archivo de texto
# Uso: fun_tail(file, num)
def fun_tail(file, num):
    with open(file) as file:
        tail = file.readlines()[-num:]
        return ("".join(tail))

# Función para guardar texto en un archivo
# Uso: fun_touch(file, text)
def fun_save_text(file, text):
    with open(file, "w") as file:
        file.write(text)


# ======================================================
# RUN
# ======================================================

def main():
    # Movernos al directorio de trabajo
    os.chdir(base_dir)

    # Crear directorio temporal
    os.makedirs('.tmp', exist_ok=True)
    
    # Contar los registros que tiene "log_file"
    record_start = fun_count_lines(log_file)
    print(f"Log antiguos: {record_start}")

    # Bucle para comprobar si hay nuevos registros, cada X segundos especificado en la variable "countdow"
    # countdown = 3
    while True:
        # Limpiar pantalla
        os.system("clear")

        exec_curr = time.strftime("%Y/%m/%d - %H:%M:%S", time.gmtime())
        print(f"Ejecutado: {exec_curr}")

        # Calcular las nuevas lineas desde la última vez que se comprobó
        # record_end = 20
        record_end = fun_count_lines(log_file)
        record_diff = fun_diff_num(record_end, record_start)
        print(f"Registros nuevos: {record_diff}\n")

        # Si record_diff es > que 0 ejecutar lo siguiente
        if record_diff > 0:

            # Salvar los nuevos registros en el archivo "alert.log"
            records = fun_tail(log_file, record_diff)
            
            fun_save_text(tmp_file, records)
            print(records)
            
            # Etablecer record_start con las nuevas lineas
            record_start = fun_count_lines(log_file)


        # Tiempo de espera (countdown) antes de volver a ejecutar
        exec_new = time.strftime("%Y/%m/%d - %H:%M:%S", time.gmtime(time.time() + 3))
        print(f"\nProxima ejecución: {exec_new}\n")
        time.sleep(countdown)

if __name__ == "__main__":
    main()