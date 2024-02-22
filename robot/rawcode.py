from flask import Flask, Response
import cv2
from robot_handler.serial_studio import SerialStudio
from robot_handler.face import Expressions
from time import sleep
import threading
import tkinter as tk
from tkinter import ttk, messagebox, font
from PIL import Image, ImageTk
from PIL.ImageTk import PhotoImage
from pyzbar import pyzbar

app = Flask(__name__)

cap = cv2.VideoCapture(0)

serstdio = SerialStudio(9600)
face = Expressions(0, 0, 255)
face.happy()
sleep(3)


def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def run_flask():
    app.run(debug=True, threaded=True, host='0.0.0.0')


def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Horizontal flip
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


# Create the main window
root = tk.Tk()
root.title("Lector de Códigos de Barras")

# Configure the window for fullscreen
root.state('zoomed')

# Create the sidebar with a larger width
sidebar_width = 300
sidebar = ttk.Frame(root, width=sidebar_width)
sidebar.pack(side=tk.LEFT, fill=tk.Y, anchor='nw')

# Configure style and font for the Listbox
listbox_font = font.Font(size=14)
listbox = tk.Listbox(sidebar, font=listbox_font)
listbox.pack(expand=True, fill=tk.BOTH)

# Button to delete a selected item
delete_button = tk.Button(sidebar, text="Eliminar", command=delete_selected)
delete_button.pack(pady=10)

# Create a frame for the camera that occupies the remaining space
camera_frame = ttk.Frame(root)
camera_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a label inside the camera_frame to display the video
label = ttk.Label(camera_frame)
label.pack(fill=tk.BOTH, expand=True)

# Start the Flask app in a separate thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

# Start the function to show the frame
show_frame()

# Start the main GUI loop
root.mainloop()
