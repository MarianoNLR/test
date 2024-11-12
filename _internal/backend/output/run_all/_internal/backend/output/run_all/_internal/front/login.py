import tkinter as tk
from tkinter import messagebox
from frontend_utils import load_image, open_script
import requests
from PIL import Image, ImageTk
from doctora import mostrar_pagina_doctora
from profesional_page import mostrar_pagina_profesional
from secretaria_page import mostrar_pagina_secretaria
import base64
import json

# Función para manejar el login
def login():
    email = entry_email.get()
    password = entry_password.get()

    # URL del nuevo endpoint de autenticación
    url = "http://127.0.0.1:8000/auth/login"
    data = {
        "email": email,
        "password": password
    }

    try:
        # Solicitud POST para autenticación
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            token = result.get("access_token")
            rol = result.get("rol", "")
            if rol:
                print(f"Rol detectado: {rol}")
                messagebox.showinfo("Login Success", "Bienvenido")

                # Dependiendo del rol, abrir la ventana correspondiente
                root.destroy()  # Cierra la ventana de login
                if rol == "Doctora":
                    mostrar_pagina_doctora(token)  # Pasa el token a la función
                elif rol == "Profesional":
                    mostrar_pagina_profesional(token)
                elif rol == "Secretaria":
                    mostrar_pagina_secretaria(token)
                else:
                    messagebox.showerror("Error", "Rol no reconocido.")
            else:
                messagebox.showerror("Error", "No se encontró el rol en la respuesta.")
        else:
            messagebox.showerror("Login Failed", "Correo o contraseña incorrectos")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"No se pudo conectar a la API: {e}")

# Configuración de la interfaz de Tkinter
root = tk.Tk()
root.title("Login")
root.state('zoomed')  # Maximizar la ventana

# Cargar la imagen de fondo usando la función load_image desde frontend_utils.py
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

# Crear un frame para las etiquetas y campos de entrada
frame_login = tk.Frame(root, bg='pink', padx=40, pady=40)
frame_login.place(relx=0.5, rely=0.5, anchor='center')  # Centrar el frame en la ventana

# Etiquetas y campos de entrada dentro del frame
label_email = tk.Label(frame_login, text="Email", bg='pink')
label_email.pack(pady=(0, 10))

entry_email = tk.Entry(frame_login)
entry_email.pack(pady=(0, 20))

label_password = tk.Label(frame_login, text="Password", bg='pink')
label_password.pack(pady=(0, 10))

entry_password = tk.Entry(frame_login, show="*")
entry_password.pack(pady=(0, 20))

# Botón de Login
button_login = tk.Button(frame_login, text="Login", command=login)
button_login.pack(pady=(0, 10))

# Botón de registro que abre register.py
button_signup = tk.Button(frame_login, text="Registrarse", command=lambda: open_script('register.py'))
button_signup.pack()

# Ejecutar la interfaz de Tkinter
root.mainloop()
