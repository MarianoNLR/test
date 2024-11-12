import datetime
import tkinter as tk
from tkinter import Canvas, messagebox
from PIL import ImageTk, Image
import requests
from frontend_utils import load_image
import base64
import json

# Función para decodificar el token
def decodificar_token(token):
    try:
        # Decodificar el token base64
        token_bytes = base64.b64decode(token.encode('utf-8'))
        token_str = token_bytes.decode('utf-8')
        # Convertir la cadena JSON en un diccionario
        data = json.loads(token_str)
        return data
    except Exception as e:
        print(f"Error al decodificar el token: {e}")
        return None

class ProfesionalPage:
    def __init__(self, root, token):
        self.root = root
        self.root.title("Página del Profesional")
        self.root.state('zoomed')

        # Decodificar el token para obtener información del usuario
        datos_usuario = decodificar_token(token)
        if datos_usuario:
            nombre_usuario = datos_usuario.get('nombre', 'Profesional')
        else:
            nombre_usuario = 'Profesional'

        # ==================== Cargar la imagen de fondo =======================
        self.cargar_fondo()

        # ==================== Header con nombre del profesional =======================
        self.header = tk.Frame(self.root, bg='#98a65d', height=80)
        self.header.pack(fill='x')

        self.title = tk.Label(
            self.header, text=f"Bienvenido, {nombre_usuario}",
            font=("Arial", 24, "bold"), bg="#98a65d", fg="white"
        )
        self.title.place(x=80, y=20)

        # ==================== Menú Lateral =======================
        self.side_menu = tk.Frame(self.root, bg="pink", width=250)
        self.side_menu.pack(side='left', fill='y')

        # Botón para ocultar/mostrar el menú lateral
        self.btn_toggle_menu = tk.Button(
            self.header, text="☰", font=("Arial", 16),
            command=self.toggle_menu, bg="#98a65d", fg="white"
        )
        self.btn_toggle_menu.place(x=20, y=20)

        # Botón para ver citas totales
        self.btn_ver_citas_totales = tk.Button(
            self.side_menu, text="Ver Citas Totales", font=("Arial", 16),
            bg="pink", fg="black", bd=0, cursor="hand2",
            command=self.mostrar_todas_citas
        )
        self.btn_ver_citas_totales.place(x=20, y=60, width=200, height=40)

        # Botón para ver citas del día
        self.btn_ver_citas_dia = tk.Button(
            self.side_menu, text="Ver Citas del Día", font=("Arial", 16),
            bg="pink", fg="black", bd=0, cursor="hand2",
            command=self.ver_citas_dia
        )
        self.btn_ver_citas_dia.place(x=20, y=120, width=200, height=40)

        # Botón para generar reportes
        self.btn_generar_reportes = tk.Button(
            self.side_menu, text="Generar Reportes", font=("Arial", 16),
            bg="pink", fg="black", bd=0, cursor="hand2",
            command=self.ingresos_rango_fecha
        )
        self.btn_generar_reportes.place(x=20, y=180, width=200, height=40)

        # Botón para "Atrás"
        self.btn_atras = tk.Button(
            self.side_menu, text="Atrás", font=("Arial", 16),
            bg="pink", fg="black", bd=0, cursor="hand2",
            command=self.atras
        )
        self.btn_atras.place(x=20, y=240, width=200, height=40)

        # ==================== Área principal =======================
        self.content = tk.Frame(self.root)
        self.content.pack(side="left", fill="both", expand=False)

    def cargar_fondo(self):
        # Crear un canvas para la imagen de fondo
        self.canvas = Canvas(
            self.root, width=self.root.winfo_screenwidth(),
            height=self.root.winfo_screenheight()
        )
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

        bg_frame = load_image('fondo1.jpg')   # Asegúrate de que esta función esté correctamente definida

        if bg_frame:
            # Ajustar el tamaño de la imagen al tamaño de la ventana
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            bg_frame = bg_frame.resize(
                (screen_width, screen_height), Image.Resampling.LANCZOS
            )

            # Guardar la imagen como un atributo de la clase para que no sea recolectada
            self.photo = ImageTk.PhotoImage(bg_frame)

            # Colocar la imagen en el canvas
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
            print("Imagen cargada y colocada en el canvas.")  # Mensaje de depuración

            # Crear un rectángulo con color semitransparente
            self.canvas.create_rectangle(
                0, 0, screen_width, screen_height, fill="#000000", stipple='gray25'
            )
        else:
            print("No se pudo cargar la imagen de fondo.")  # Mensaje de depuración

        # Forzar la actualización de la ventana
        self.root.update_idletasks()

    def toggle_menu(self):
        if self.side_menu.winfo_viewable():
            self.side_menu.pack_forget()  # Ocultar el menú lateral
        else:
            self.side_menu.pack(side="left", fill="y")  # Mostrar en el lado izquierdo
        for widget in self.content.winfo_children():
            widget.destroy()
        self.content.destroy()
        self.content = tk.Frame(self.root)
        self.content.pack(side="left", fill="both", expand=False)

    def mostrar_todas_citas(self):
        # Limpiar el área principal y mostrar todas las citas
        for widget in self.content.winfo_children():
            widget.destroy()
        # Llamada a la API para obtener citas
        url = "http://127.0.0.1:8000/reservas/total"
        encabezados = ["Cliente", "Servicio", "Trabajador", "Fecha"]
        campos = ["Cliente", "Servicio", "Trabajador", "fecha"]
        self.mostrar_datos_api(url, encabezados, campos)

    def ver_citas_dia(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        citas_dia_label = tk.Label(self.content, text="Ver Citas del Día", font=("Arial", 20))
        citas_dia_label.pack(pady=1)
        encabezados = ["Cliente", "Servicio", "Trabajador", "Fecha"]
        campos = ["cliente", "servicio", "trabajador", "fecha"]
        url = "http://127.0.0.1:8000/reservas/dia"
        self.mostrar_datos_api(url, encabezados, campos)

    def ingresos_rango_fecha(self):
        # Limpia el contenido actual
        for widget in self.content.winfo_children():
            widget.destroy()

        # Título
        ingresos_label = tk.Label(self.content, text="Ingresos en un Rango de Fecha", font=("Arial", 20))
        ingresos_label.pack(pady=1)

        # Campo de entrada para fecha de inicio
        self.fecha_inicio_label = tk.Label(self.content, text="Ingresar Fecha inicio:", font=("Arial", 14))
        self.fecha_inicio_label.pack(pady=5)
        self.fecha_inicio_entry = tk.Entry(self.content, font=("Arial", 14))
        self.fecha_inicio_entry.pack(pady=5)

        # Campo de entrada para fecha de fin
        self.fecha_fin_label = tk.Label(self.content, text="Ingresar Fecha fin:", font=("Arial", 14))
        self.fecha_fin_label.pack(pady=5)
        self.fecha_fin_entry = tk.Entry(self.content, font=("Arial", 14))
        self.fecha_fin_entry.pack(pady=5)

        # Botón para buscar datos y llamar a la función con las fechas ingresadas
        descargar_button = tk.Button(
            self.content,
            text="DESCARGAR",
            command=lambda: self.mostrar_datos_api2(
                f"http://127.0.0.1:8000/informe/ingresos/{self.fecha_inicio_entry.get()}/{self.fecha_fin_entry.get()}",
            )
        )
        descargar_button.pack(pady=10)

    def mostrar_datos_api2(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                messagebox.showinfo("Completado", "PDF descargado en el rango de fecha seleccionado")
            else:
                messagebox.showerror("Error", f"Error al obtener datos de la API: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un problema al conectar con la API: {e}")

    def mostrar_datos_api(self, url, encabezados, campos):
        # Método general para obtener datos de la API y mostrarlos en formato de tabla.
        try:
            response = requests.get(url)
            if response.status_code == 200:
                datos = response.json()
                if len(datos) == 0:
                    messagebox.showinfo("Sin resultados", "No se encontraron resultados para la solicitud.")
                    return

                # Limpiar el área de contenido para mostrar los resultados
                for widget in self.content.winfo_children():
                    widget.destroy()

                # Crear un Frame semitransparente para los resultados
                resultados_frame = tk.Frame(self.content, bg="white", bd=2)
                resultados_frame.grid(row=0, column=0, pady=10, padx=10, sticky="n")

                # Configuración para que las columnas se expandan horizontalmente, pero no las filas
                self.content.grid_columnconfigure(0, weight=1)
                resultados_frame.grid_columnconfigure(0, weight=1)
                for col_idx in range(len(encabezados)):
                    resultados_frame.grid_columnconfigure(col_idx, weight=1)

                # Título de los resultados
                resultados_label = tk.Label(
                    resultados_frame, text="Resultados", font=("Arial", 10), bg="#00CC66", fg="white"
                )
                resultados_label.grid(row=0, column=0, columnspan=len(encabezados), pady=10, sticky="ew")

                # Mostrar encabezados
                for idx, encabezado in enumerate(encabezados):
                    tk.Label(
                        resultados_frame, text=encabezado, font=("Arial", 14, "bold"),
                        bg="#00CC66", fg="white", width=20, relief="solid", anchor="w", padx=5
                    ).grid(row=1, column=idx, padx=5, pady=5, sticky="ew")

                # Mostrar los resultados
                for row_idx, fila in enumerate(datos, start=2):
                    for col_idx, campo in enumerate(campos):
                        tk.Label(
                            resultados_frame, text=fila.get(campo, "Desconocido"), font=("Arial", 12),
                            bg="white", width=10, anchor="w", relief="solid", padx=5
                        ).grid(row=row_idx, column=col_idx, padx=5, pady=5, sticky="ew")
            else:
                messagebox.showerror("Error", f"Error al obtener datos de la API: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un problema al conectar con la API: {e}")

    def atras(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        self.content.destroy()
        self.content = tk.Frame(self.root)
        self.content.pack(side="left", fill="both", expand=False)

# Para ejecutar la ventana de profesional
def mostrar_pagina_profesional(token):
    root = tk.Tk()
    ProfesionalPage(root, token)
    root.mainloop()
