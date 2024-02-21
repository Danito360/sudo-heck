import tkinter as tk
from tkinter import filedialog
import os
from urllib.request import urlopen
from urllib.error import URLError
from tqdm import tqdm

FILES_DIRECTORY = "Files"  # Directorio donde se descargarán los archivos

def get_next_number():
    if not os.path.exists('sudoheck-data.heck'):
        return 1
    with open('sudoheck-data.heck', 'r') as f:
        lines = f.readlines()
        if lines:
            last_line = lines[-1]
            last_number = int(last_line.split("-")[0])
            return last_number + 1
        else:
            return 1

def add_entry():
    nombre = entry_nombre.get().strip()
    enlace = entry_enlace.get().strip()
    if nombre and enlace:
        next_number = get_next_number()
        with open('sudoheck-data.heck', 'a+') as f:
            f.write(f"{next_number}-{nombre}-{enlace}\n")
        entry_nombre.delete(0, tk.END)
        entry_enlace.delete(0, tk.END)
        load_entries()
    else:
        status_label.config(text="Por favor, introduce un nombre y un enlace.", fg="red")

def add_links_to_last_entry():
    enlaces = entry_links.get().strip().split(",")
    if enlaces:
        with open('sudoheck-data.heck', 'a+') as f:
            f.seek(0)
            lines = f.readlines()
            if lines:
                last_line = lines[-1].strip().split("-")
                last_number = last_line[0]
                last_name = last_line[1]
                last_links = last_line[2]
                for enlace in enlaces:
                    last_links += f",{enlace}"
                lines[-1] = f"{last_number}-{last_name}-{last_links}\n"
                f.seek(0)
                f.truncate()
                f.writelines(lines)
        entry_links.delete(0, tk.END)
        load_entries()
    else:
        status_label.config(text="Por favor, introduce al menos un enlace.", fg="red")

def verify_downloadable():
    for widget in frame_entries.winfo_children():
        widget.destroy()

    with open('sudoheck-data.heck', 'r') as f:
        for line in f:
            numero, nombre, enlace = line.strip().split('-')
            try:
                response = urlopen(enlace)
                status = response.getcode()
                if status == 200:
                    message = f"El archivo en el enlace {enlace} es descargable."
                    color = "green"
                else:
                    message = f"El archivo en el enlace {enlace} no es descargable (Código de estado: {status})."
                    color = "red"
            except URLError as e:
                message = f"El archivo en el enlace {enlace} no es descargable: {e.reason}."
                color = "red"
            label = tk.Label(frame_entries, text=f"{numero}: {nombre} ({enlace})", wraplength=400, justify=tk.LEFT)
            label.grid(row=int(numero), column=1, sticky="w")
            tk.Label(frame_entries, text=message, wraplength=400, justify=tk.LEFT, fg=color).grid(row=int(numero), column=2, sticky="w")
            tk.Button(frame_entries, text="Eliminar", command=lambda num=numero: delete_entry(num)).grid(row=int(numero), column=0, sticky="w")

def delete_entry(numero):
    with open('sudoheck-data.heck', 'r') as f:
        lines = f.readlines()
    with open('sudoheck-data.heck', 'w') as f:
        for line in lines:
            if not line.startswith(f"{numero}-"):
                f.write(line)
    load_entries()

def load_entries():
    for widget in frame_entries.winfo_children():
        widget.destroy()

    with open('sudoheck-data.heck', 'r') as f:
        for line in f:
            numero, nombre, enlace = line.strip().split('-')
            label = tk.Label(frame_entries, text=f"{numero}: {nombre} ({enlace})", wraplength=400, justify=tk.LEFT)
            label.grid(row=int(numero), column=1, sticky="w")
            tk.Button(frame_entries, text="Eliminar", command=lambda num=numero: delete_entry(num)).grid(row=int(numero), column=0, sticky="w")

root = tk.Tk()
root.title("Gestor de Archivos")
root.geometry("800x600")
root.configure(bg="#333333")

# Cargar el logo
logo = tk.PhotoImage(file="logo.png")
logo_label = tk.Label(root, image=logo, bg="#333333")
logo_label.pack()

# Formulario de agregar entrada
add_frame = tk.Frame(root, bg="#333333")
add_frame.pack(pady=10)

tk.Label(add_frame, text="Nombre:", fg="white", bg="#333333").grid(row=0, column=0, padx=10, pady=5, sticky="e")
tk.Label(add_frame, text="Enlace:", fg="white", bg="#333333").grid(row=1, column=0, padx=10, pady=5, sticky="e")

entry_nombre = tk.Entry(add_frame, width=40)
entry_enlace = tk.Entry(add_frame, width=40)
entry_nombre.grid(row=0, column=1, padx=10, pady=5)
entry_enlace.grid(row=1, column=1, padx=10, pady=5)

tk.Button(add_frame, text="Agregar", command=add_entry, bg="#555555", fg="white", padx=10, pady=5).grid(row=2, column=1, pady=10)

# Botón para agregar enlaces a la última entrada
tk.Label(root, text="Agregar enlaces a la última entrada:", fg="white", bg="#333333").pack()
entry_links = tk.Entry(root, width=40)
entry_links.pack(pady=5)
tk.Button(root, text="Agregar Enlaces", command=add_links_to_last_entry, bg="#555555", fg="white", padx=10, pady=5).pack(pady=5)

# Botón para verificar si los archivos son descargables
tk.Button(root, text="Verificar Descargabilidad", command=verify_downloadable, bg="#555555", fg="white", padx=10, pady=5).pack(pady=5)

# Botón para abrir archivo
open_frame = tk.Frame(root, bg="#333333")
open_frame.pack()

tk.Button(open_frame, text="Abrir sudoheck-data.heck", command=lambda: os.startfile('sudoheck-data.heck'), bg="#555555", fg="white", padx=10, pady=5).pack(pady=5)

# Sección para mostrar entradas
frame_entries = tk.Frame(root, bg="#333333")
frame_entries.pack(expand=True, fill="both")

status_label = tk.Label(root, text="", fg="red", bg="#333333")
status_label.pack(pady=5)

root.mainloop()
