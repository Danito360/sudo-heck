import tkinter as tk
from tkinter import filedialog
import os
from urllib.request import urlretrieve
from tqdm import tqdm

FILES_DIRECTORY = "Files"  # Directorio donde se descargarán los archivos

def add_entry():
    nombre = entry_nombre.get().strip()
    enlace = entry_enlace.get().strip()
    if nombre and enlace:
        with open('sudoheck-data.heck', 'a') as f:
            f.write(f"{len(entries)+1}-{nombre}-{enlace}\n")
        entry_nombre.delete(0, tk.END)
        entry_enlace.delete(0, tk.END)
        load_entries()
    else:
        status_label.config(text="Por favor, introduce un nombre y un enlace.", fg="red")

def load_entries():
    for entry in entries:
        entry.destroy()

    with open('sudoheck-data.heck', 'r') as f:
        lines = sorted(f.readlines(), key=lambda x: x.split('-')[1].lower())  # Ordenar por nombre
        for line in lines:
            numero, nombre, enlace = line.strip().split('-')
            tk.Label(frame_entries, text=f"{numero}: {nombre} ({enlace})", wraplength=400, justify=tk.LEFT).pack(anchor="w")
            tk.Button(frame_entries, text="Descargar", command=lambda e=enlace: download_file(e, nombre)).pack(anchor="w")

def download_file(url, filename):
    filepath = os.path.join(FILES_DIRECTORY, filename)
    print(f"Descargando {url} como {filepath}...")
    if not os.path.exists(FILES_DIRECTORY):
        os.makedirs(FILES_DIRECTORY)
    with tqdm(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc=filename) as t:
        def update_to(count, block_size, total_size):
            t.update(count * block_size - t.n)
        urlretrieve(url, filepath, reporthook=update_to)

def add_entry_window():
    global add_window
    add_window = tk.Toplevel(root)
    add_window.title("Añadir Entrada")
    add_window.geometry("400x150")

    tk.Label(add_window, text="Nombre:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    tk.Label(add_window, text="Enlace:").grid(row=1, column=0, padx=10, pady=5, sticky="e")

    global entry_nombre, entry_enlace
    entry_nombre = tk.Entry(add_window, width=40)
    entry_enlace = tk.Entry(add_window, width=40)
    entry_nombre.grid(row=0, column=1, padx=10, pady=5)
    entry_enlace.grid(row=1, column=1, padx=10, pady=5)

    tk.Button(add_window, text="Agregar", command=add_entry).grid(row=2, column=1, pady=10)
    add_window.mainloop()

def open_file():
    filepath = filedialog.askopenfilename(initialdir=os.getcwd(), title="Selecciona el archivo", filetypes=(("Archivos de texto", "*.heck"), ("Todos los archivos", "*.*")))
    if filepath:
        os.startfile(filepath)

root = tk.Tk()
root.title("Gestor de Archivos")
root.geometry("600x400")
root.configure(bg="#333333")

# Cargar el logo
logo = tk.PhotoImage(file="logo.png")
logo_label = tk.Label(root, image=logo, bg="#333333")
logo_label.pack()

tk.Button(root, text="Añadir Entrada", command=add_entry_window, bg="#555555", fg="white", padx=10, pady=5).pack(pady=10)
tk.Button(root, text="Abrir sudoheck-data.heck", command=open_file, bg="#555555", fg="white", padx=10, pady=5).pack()

frame_entries = tk.Frame(root, bg="#333333")
frame_entries.pack()

status_label = tk.Label(root, text="", fg="red", bg="#333333")
status_label.pack(pady=5)

entries = []

load_entries()

root.mainloop()
