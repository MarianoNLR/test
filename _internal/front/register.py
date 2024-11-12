"""Importaciones varias"""
import tkinter as tk
from tkinter import messagebox
from frontend_utils import load_image  # Importar la función para cargar imágenes
import requests
from PIL import Image, ImageTk

# Función para el evento de registro
def registrar_usuario():
    nombre = entry_nombre.get()
    email = entry_email.get()
    telefono = entry_telefono.get()
    password = entry_password.get()  # Obtener la contraseña (password)
    rol = "cliente"
    if nombre and email and telefono and password:
        # Crear el payload con los datos de registro
        data = {
            "nombre": nombre,
            "email": email,
            "telefono": telefono,
            "password": password,
            "rol":rol # Añadir el password al payload
        }
        try:
            # Hacer la solicitud POST a la API
            response = requests.post("http://127.0.0.1:8000/clients/", json=data)
            root.withdraw()
            # Verificar si el registro fue exitoso
            if response.status_code == 200:
                messagebox.showinfo("Registro", "Registro exitoso")

            else:
                messagebox.showerror("Error", f"Error en el registro: {response.json().get('message')}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la API: {e}")
    else:
        messagebox.showerror("Error", "Por favor, completa todos los campos")

# Crear la ventana principal
root = tk.Tk()
root.title("Registro de Usuario")
root.geometry('1266x712')
# Maximizar la ventana sin ser pantalla completa

# Cargar la imagen de fondo usando la función load_image() desde frontend_utils.py
bg_frame = load_image('fondo1.jpg')
if bg_frame:
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    bg_frame = bg_frame.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(bg_frame)

    # Crear el label para la imagen de fondo
    bg_panel = tk.Label(root, image=photo)
    bg_panel.image = photo  # Mantener la referencia de la imagen
    bg_panel.place(x=0, y=0, relwidth=1, relheight=1)  # Ajustar la imagen a toda la ventana

# Etiqueta y campo de entrada para el nombre de usuario
label_nombre = tk.Label(root, text="Nombre:")
label_nombre.pack(pady=5)
entry_nombre = tk.Entry(root)
entry_nombre.pack(pady=5)

# Etiqueta y campo de entrada para el correo electrónico
label_email = tk.Label(root, text="Correo Electrónico:")
label_email.pack(pady=5)
entry_email = tk.Entry(root)
entry_email.pack(pady=5)

# Etiqueta y campo de entrada para el teléfono
label_telefono = tk.Label(root, text="Teléfono:")
label_telefono.pack(pady=5)
entry_telefono = tk.Entry(root)
entry_telefono.pack(pady=5)

# Etiqueta y campo de entrada para la password
label_password = tk.Label(root, text="Password:")
label_password.pack(pady=5)
entry_password = tk.Entry(root, show="*")  # El campo "show='*'" enmascara la entrada
entry_password.pack(pady=5)

# Botón para registrar
button_register = tk.Button(root, text="Registrar", command=registrar_usuario)
button_register.pack(pady=20)

# Iniciar la ventana principal
root.mainloop()