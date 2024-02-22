import tkinter as tk
from tkinter import ttk, messagebox, font
import cv2
from PIL import Image, ImageTk
from pyzbar import pyzbar

def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    barcodes = pyzbar.decode(frame)

    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        barcode_data = barcode.data.decode('utf-8')
        if barcode_data not in barcode_list:
            barcode_list.append(barcode_data)
            listbox.insert(tk.END, barcode_data)
            messagebox.showinfo("Registro", "Código de barras registrado!")

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    label.imgtk = imgtk
    label.configure(image=imgtk)
    label.after(10, show_frame)

def delete_selected():
    try:
        selected = listbox.curselection()
        listbox.delete(selected[0])
    except IndexError:
        messagebox.showwarning("Advertencia", "Por favor, selecciona un elemento para eliminar.")

def on_closing():
    cap.release()
    root.destroy()

# Crear la ventana principal
root = tk.Tk()
root.title("Lector de Códigos de Barras")

# Configurar la ventana para pantalla completa
root.attributes('-zoomed', True)

# Crear el sidebar con un ancho más grande
sidebar_width = 300
sidebar = ttk.Frame(root, width=sidebar_width)
sidebar.pack(side=tk.LEFT, fill=tk.Y, anchor='nw')

# Configurar el estilo y la fuente para el Listbox
listbox_font = font.Font(size=14)
listbox = tk.Listbox(sidebar, font=listbox_font)
listbox.pack(expand=True, fill=tk.BOTH)

# Botón para eliminar un elemento seleccionado
delete_button = tk.Button(sidebar, text="Eliminar", command=delete_selected)
delete_button.pack(pady=10)

# Inicializar la captura de video
cap = cv2.VideoCapture(0)

# Crear un frame para la cámara que ocupe todo el espacio restante
camera_frame = ttk.Frame(root)
camera_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Crear un label dentro del camera_frame donde se mostrará el video
label = ttk.Label(camera_frame)
label.pack(fill=tk.BOTH, expand=True)

# Iniciar la función para mostrar el frame
show_frame()

# Configurar el manejo de cierre
root.protocol("WM_DELETE_WINDOW", on_closing)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
import tkinter as tk
from tkinter import ttk, messagebox, font
import cv2
from PIL import Image, ImageTk
from pyzbar import pyzbar

def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    barcodes = pyzbar.decode(frame)

    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        barcode_data = barcode.data.decode('utf-8')
        if barcode_data not in barcode_list:
            barcode_list.append(barcode_data)
            listbox.insert(tk.END, barcode_data)
            messagebox.showinfo("Registro", "Código de barras registrado!")

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    label.imgtk = imgtk
    label.configure(image=imgtk)
    label.after(10, show_frame)

def delete_selected():
    try:
        selected = listbox.curselection()
        listbox.delete(selected[0])
    except IndexError:
        messagebox.showwarning("Advertencia", "Por favor, selecciona un elemento para eliminar.")

def on_closing():
    cap.release()
    root.destroy()

# Crear la ventana principal
root = tk.Tk()
root.title("Lector de Códigos de Barras")

# Configurar la ventana para pantalla completa
root.attributes('-zoomed', True)

# Crear el sidebar con un ancho más grande
sidebar_width = 300
sidebar = ttk.Frame(root, width=sidebar_width)
sidebar.pack(side=tk.LEFT, fill=tk.Y, anchor='nw')

# Configurar el estilo y la fuente para el Listbox
listbox_font = font.Font(size=14)
listbox = tk.Listbox(sidebar, font=listbox_font)
listbox.pack(expand=True, fill=tk.BOTH)

# Botón para eliminar un elemento seleccionado
delete_button = tk.Button(sidebar, text="Eliminar", command=delete_selected)
delete_button.pack(pady=10)

# Inicializar la captura de video
cap = cv2.VideoCapture(0)

# Crear un frame para la cámara que ocupe todo el espacio restante
camera_frame = ttk.Frame(root)
camera_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Crear un label dentro del camera_frame donde se mostrará el video
label = ttk.Label(camera_frame)
label.pack(fill=tk.BOTH, expand=True)

# Iniciar la función para mostrar el frame
show_frame()

# Configurar el manejo de cierre
root.protocol("WM_DELETE_WINDOW", on_closing)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
