# Instalar el paquete pyenv para crear entornos virtuales
    pacman -S pyenv

# Crear nuestro entorno virtual
    python3 -m venv tu_proyecto

# Activar el entorno virtual
    source tu_proyecto/bin/activate

- https://python-docs-es.readthedocs.io/es/3.9/library/functions.html?highlight=funciones%20integradas#open

Leer archivo de texto con la función `open()`, los métodos  `read()`, `readline()`, `readlines()`, `close()` y la palabra clave `with`.
# Abrir archivo
    open("lista_compras.txt")

Modos de apertura con la función `open()`, el modo por defecto es el de  modo lectura `"r"`.
- `r` abierto para lectura (por defecto)
- `w` abierto para escritura, truncando primero el fichero
- `x` abierto para creación en exclusiva, falla si el fichero ya existe
- `a` abierto para escritura, añadiendo al final del fichero si este existe
- `b` modo binario
- `t` modo texto (por defecto)
- `+` abierto para actualizar (lectura y escritura)
open("lista_compras.txt", "r")

El método `readable()` (legible), se usa para saber si un archivo se puede leer.

El siguiente ejemplo devolverá True, porque estamos en el modo lectura por defecto.

```python
archivo = open("lista_compras.txt")
print(archivo.readable())

True
```

El método `read()` leerá todo el contenido de un archivo y lo devolverá como una cadena de texto, Este es una buena forma de leer un archivo solo si tu archivo de texto no es muy grande.
```python
archivo = open("lista_compras.txt")
print(archivo.read())

Cosas por comprar:
Arroz
leche
huevos
agua
```

Este método acepta un parámetro adicional donde podemos especificar el número de caracteres a leer. 

Modificando el ejemplo anterior,  podremos imprimir solo la primera palabra, añadiendo el número `5` como argumento de `read()`

```python
archivo = open("lista_compras.txt")
print(archivo.read(5))
Cosas
```
El método close(), una vez terminaste de leer un archivo, es importante cerrarlo, de otra forma el archivo se queda abierto, lo cual puede generar problemas

```python
archivo = open("lista_compras.txt")
print(archivo.read(5))
archivo.close()
```

Una forma de asegurar que tu archivo es cerrado, es  usar la palabra clave `with`. Su uso es considerado una  buena práctica, porque el archivo se cierra automáticamente en lugar de tener que cerrarlo manualmente. Con `as` estamos diciendo como llamaremos a `open("lista_compras.txt")` 

```python
with open("lista_compras.txt") as archivo:
    print(archivo.read())
```

El método `readline()` leerá una línea del archivo y la devolverá. En este ejemplo, tenemos un archivo con dos enunciados.

    Esta es la primera linea
    Esta es la segunda linea

Si usamos el método `readline()`, imprimirá solo la primera sentencia.

```python
with open("prueba.txt") as archivo:
    print(archivo.readline())
Esta es la primera linea
```

El método readline() acepta un parámetro opcional donde podemos especificar el número de caracteres a leer. Añadiendo el número `7` a `readline()` para leer solo caracteres:

```python
with open("demo.txt") as file:
    print(file.readline(7))
Esta es
```

El método readlines() devolverá una lista de todas las líneas de texto del archivo
En este ejemplo, Imprimiremos lista_compras.txt como una lista usando el método 
`readlines()`

```python
with open("lista_compras.txt") as archivo:
    print(archivo.readlines())
["Cosas por comprar:\n","Arroz\n", "leche\n", "huevos\n", "agua\n"]
```

Usar un bucle `for` para leer cada línea de texto de un archivo. En este ejemplo, podemos imprimir cada línea de texto de `lista_compras.txt` iterando sobre el objeto archivo.

```python
with open("lista_compras.txt") as archivo:
    for linea in archivo:
        print(linea)

Cosas por comprar:
Arroz
leche
huevos
agua
```