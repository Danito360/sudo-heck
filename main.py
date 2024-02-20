print("Bienvenido a SUDO HECK, para comenzar escriba ")
import argparse
from urllib.request import urlretrieve
from tqdm import tqdm
import os
import re

FILES_DIRECTORY = "Files"  # Directorio donde se descargarán los archivos

def download_with_progress(url, filename):
    # Descarga el archivo y obtén su tamaño total en bytes
    with tqdm(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc=filename) as t:
        def update_to(count, block_size, total_size):
            t.update(count * block_size - t.n)
        urlretrieve(url, filename, reporthook=update_to)

def download_file(url, filename):
    filepath = os.path.join(FILES_DIRECTORY, filename)
    print(f"Descargando {url} como {filepath}...")
    if not os.path.exists(FILES_DIRECTORY):
        os.makedirs(FILES_DIRECTORY)
    download_with_progress(url, filepath)

def delete_file(filename):
    filepath = os.path.join(FILES_DIRECTORY, filename)
    secure = input(f"¿Estás seguro de que quieres eliminar: {filename} de {filepath}? Y/N: ")
    if secure.lower() == "y":
        print(f"Eliminando {filepath}...")
        os.remove(filepath)
    else:
        print("No se realizará ninguna acción.")

def list_files(directory):
    print("Archivos en el subdirectorio 'Files':")
    r = 1
    for file in os.listdir(directory):
        print("[",r,"]", file)
        r = r + 1

def procesar_linea(linea):
    partes = linea.strip().split("-")
    numero_archivo = partes[0]
    nombre_archivo = partes[1]
    enlace = partes[2]
    return numero_archivo, nombre_archivo, enlace

def procesar_archivo(archivo, search_term):
    archivos_encontrados = []
    with open(archivo, 'r') as f:
        for linea in f:
            numero_archivo, nombre_archivo, enlace = procesar_linea(linea)
            if search_term.lower() in nombre_archivo.lower():
                archivos_encontrados.append((numero_archivo, nombre_archivo, enlace))

    if not archivos_encontrados:
        print("No se encontraron archivos que coincidan con el término de búsqueda.")
        return

    if len(archivos_encontrados) > 1:
        print("Se encontraron múltiples archivos que coinciden con el término de búsqueda:")
        for numero, nombre, _ in archivos_encontrados:
            print(f"[{numero}] {nombre}")
        numero_archivo_elegido = input("Ingrese el número del archivo que desea descargar: ")
        for numero, nombre, enlace in archivos_encontrados:
            if numero == numero_archivo_elegido:
                download_file(enlace, nombre)
                break
        else:
            print("Número de archivo no válido.")
    else:
        _, nombre_archivo, enlace = archivos_encontrados[0]
        download_file(enlace, nombre_archivo)

def intro():
    print("¡Bienvenido! Este es un programa para descargar y eliminar archivos.")
    print("Utilice 'python nombre_del_programa.py -h' para obtener ayuda sobre cómo usarlo.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Descarga o elimina un archivo según los argumentos proporcionados.')
    parser.add_argument('Action', choices=['heck', 'unheck'], nargs='?', help='Acción a realizar (heck para descargar, unheck para eliminar)')
    parser.add_argument('SearchTerm', nargs='?', default='', help='Número o nombre del archivo a buscar (ignorando mayúsculas y signos de puntuación)')
    parser.add_argument('Program', nargs='?', default='sudoheck-data.heck', help='Nombre del archivo de texto que contiene la información (por defecto: sudoheck-data.heck)')
    parser.add_argument('-l', action='store_true', help='Lista los archivos en el subdirectorio "Files"')
    args = parser.parse_args()

    if not any(vars(args).values()):  # Si no se proporciona ningún parámetro
        intro()
    elif args.l:
        list_files(FILES_DIRECTORY)
    elif args.Action == 'heck':
        if args.SearchTerm:
            procesar_archivo(args.Program, args.SearchTerm)
        else:
            print("Se requiere especificar el número o nombre del archivo a buscar.")
    elif args.Action == 'unheck':
        if args.SearchTerm:
            delete_file(args.SearchTerm)
        else:
            print("Se requiere especificar el número o nombre del archivo a eliminar.")
