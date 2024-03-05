# SUDO HECK
![logo white](https://github.com/Danito360/sudo-heck/blob/sudoheck/logo3.png)
## Sudo heck is a program for easly install videogames from a preloaded list, that means NO SEARCH, NO MALWARE, NO STRANGE WEBSITES, NO ADS and NO INSTALLATION.

Only run commands like "sudoheck heck ARK" to automatically download and install all files on your computer, without visit any webpage and open any file, all automatically

# Project in progress
# Como usar SUDOHECK

## ¿Qué hace SUDOHECK?
Bienvenido a SUDOHECK, una utilidad de descarga de archivos .heck (encriptados o no). Con SUDOHECK, puedes descargar archivos, descomprimirlos, listar los archivos en el directorio "Files", y eliminar archivos descargados. Esta guía te proporcionará los pasos básicos para utilizar SUDOHECK eficazmente.

## Pasos Básicos

### Descargar e Instalar SUDOHECK
1. Clona el repositorio de SUDOHECK desde GitHub o descarga el código fuente.
2. Asegúrate de tener instalado Python en tu sistema. Si no lo tienes, puedes descargarlo desde [python.org](https://www.python.org/downloads/).
3. Abre una terminal o línea de comandos y navega hasta el directorio donde descargaste el código de SUDOHECK.

### Ejecutar SUDOHECK
Para ejecutar SUDOHECK, sigue estos pasos:

#### Descargar un Archivo
```
python main.py heck [SearchTerm] [Program]
```
- `[SearchTerm]`: Especifica el número o nombre del archivo a buscar.
- `[Program]` (opcional): Es el nombre del archivo de texto que contiene la información. Por defecto, es `sudoheck-data.heck`.

#### Eliminar un Archivo Descargado
```
python main.py unheck [SearchTerm]
```
- `[SearchTerm]`: Especifica el número o nombre del archivo a eliminar.

#### Listar Archivos Descargados
```
python main.py -l
```
Este comando lista todos los archivos en el subdirectorio "Files".

### Consideraciones Adicionales
- Asegúrate de tener una conexión a Internet estable para descargar archivos correctamente.
- Los archivos descargados se guardarán en el directorio "Files", dentro de la carpeta SUDOHECK.

## Conclusión
Ahora que conoces los pasos básicos para usar SUDOHECK, puedes comenzar a descargar y administrar archivos .heck de manera eficiente. Para obtener más detalles sobre el uso de SUDOHECK, consulta la ayuda usando el siguiente comando:
```
python main.py -h
```
##¡Disfruta descargando y pirateando tus archivos con SUDOHECK!
