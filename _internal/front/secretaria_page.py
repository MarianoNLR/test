import datetime
import tkinter as tk
from tkinter import Canvas, messagebox
from tkinter import ttk
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

class SecretariaPage:
    def __init__(self, root, token):
        self.root = root
        self.root.title("Página de la Secretaria")
        self.root.state('zoomed')

        # Decodificar el token para obtener información del usuario
        datos_usuario = decodificar_token(token)
        if datos_usuario:
            nombre_usuario = datos_usuario.get('nombre', 'Secretaria')
        else:
            nombre_usuario = 'Secretaria'

        # ==================== Cargar la imagen de fondo =======================
        self.cargar_fondo()

        # ==================== Header con nombre de la secretaria =======================
        self.header = tk.Frame(self.root, bg='#98a65d', height=80)
        self.header.pack(fill='x')

        self.title = tk.Label(
            self.header, text=f"Bienvenida, {nombre_usuario}",
            font=("Arial", 24, "bold"), bg="#98a65d", fg="white"
        )
        self.title.place(x=80, y=20)

        # ==================== Menú Lateral =======================
        self.side_menu = tk.Frame(self.root, bg="pink", width=380)
        self.side_menu.pack(side='left', fill='y')

        # Botón para ocultar/mostrar el menú lateral
        self.btn_toggle_menu = tk.Button(
            self.header, text="☰", font=("Arial", 16),
            command=self.toggle_menu, bg="#98a65d", fg="white"
        )
        self.btn_toggle_menu.place(x=20, y=20)

        # Botón para "Crear Empleado"
        self.btn_crear_empleado = tk.Button(
            self.side_menu, text="Crear Empleado", font=("Arial", 16),
            bg="pink", fg="black", bd=0, cursor="hand2",
            command=self.crear_empleado
        )
        self.btn_crear_empleado.place(x=10, y=60, width=150, height=40)

        # Botón para "Listado de Clientes"
        self.btn_listado_clientes = tk.Button(
            self.side_menu, text="Listado de Clientes", font=("Arial", 16),
            bg="pink", fg="black", bd=0, cursor="hand2",
            command=self.listado_clientes
        )
        self.btn_listado_clientes.place(x=10, y=120, width=180, height=40)

        # Botón para "Listado de Clientes a Atender por Día"
        self.btn_listado_clientes_dia = tk.Button(
            self.side_menu, text="Listado de Clientes a Atender por Día",
            font=("Arial", 16), bg="pink", fg="black", bd=0, cursor="hand2",
            command=self.listado_clientes_dia
        )
        self.btn_listado_clientes_dia.place(x=10, y=180, width=350, height=40)

        # Botón para "Ingresos en un Rango de Fecha (DESCARGAR)"
        self.btn_ingresos_rango_fecha = tk.Button(
            self.side_menu, text="Ingresos en un Rango de Fecha",
            font=("Arial", 16), bg="pink", fg="black", bd=0, cursor="hand2",
            command=self.ingresos_rango_fecha
        )
        self.btn_ingresos_rango_fecha.place(x=10, y=240, width=300, height=40)

        # Botón para "Listado de Clientes por Profesional"
        self.btn_listado_clientes_profesional = tk.Button(
            self.side_menu, text="Listado de Clientes por Profesional",
            font=("Arial", 16), bg="pink", fg="black", bd=0, cursor="hand2",
            command=self.administrar_profesionales
        )
        self.btn_listado_clientes_profesional.place(x=10, y=300, width=330, height=40)

        # Botón para "Ver Citas del Día"
        self.btn_ver_citas_dia = tk.Button(
            self.side_menu, text="Ver Citas del Día", font=("Arial", 16),
            bg="pink", fg="black", bd=0, cursor="hand2",
            command=self.ver_citas_dia
        )
        self.btn_ver_citas_dia.place(x=8, y=360, width=170, height=40)

        # Botón para "Generar Pago"
        self.btn_generar_pago = tk.Button(
            self.side_menu, text="Generar Pago", font=("Arial", 16),
            bg="pink", fg="black", bd=0, cursor="hand2",
            command=self.generar_pago
        )
        self.btn_generar_pago.place(x=10, y=420, width=130, height=40)

        # Botón para "Crear Reserva"
        self.btn_crear_reserva = tk.Button(
            self.side_menu, text="Crear Reserva", font=("Arial", 16),
            bg="pink", fg="black", bd=0, cursor="hand2",
            command=self.crear_reserva
        )
        self.btn_crear_reserva.place(x=10, y=480, width=140, height=40)

        # Botón "Atrás"
        self.btn_atras = tk.Button(
            self.side_menu, text="Atrás", font=("Arial", 16),
            bg="pink", fg="black", bd=0, cursor="hand2",
            command=self.atras
        )
        self.btn_atras.place(x=10, y=540, width=50, height=40)

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

        bg_frame = load_image('fondo1.jpg')  # Asegúrate de que esta función esté correctamente definida

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

    def ver_citas_dia(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        citas_dia_label = tk.Label(self.content, text="Ver Citas del Día", font=("Arial", 20))
        citas_dia_label.pack(pady=1)
        encabezados = ["Cliente", "Servicio", "Trabajador", "Fecha"]
        campos = ["cliente", "servicio", "trabajador", "fecha"]
        url = "http://127.0.0.1:8000/reservas/dia"
        self.mostrar_datos_api(url, encabezados, campos)

    def mostrar_datos_api(self, url, encabezados, campos):
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

                # Crear un Frame para los resultados
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
                resultados_label.grid(
                    row=0, column=0, columnspan=len(encabezados), pady=10, sticky="ew"
                )

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

    def crear_reserva(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        # Título de la sección
        reserva_label = tk.Label(self.content, text="Crear Reserva", font=("Arial", 20))
        reserva_label.pack(pady=20)

        # Campo de texto para Cliente ID
        cliente_id_label = tk.Label(self.content, text="ID del Cliente")
        cliente_id_label.pack(pady=(10, 0))
        cliente_id_entry = tk.Entry(self.content)
        cliente_id_entry.pack()

        # Campo de texto para Servicio ID
        servicio_id_label = tk.Label(self.content, text="ID del Servicio")
        servicio_id_label.pack(pady=(10, 0))
        servicio_id_entry = tk.Entry(self.content)
        servicio_id_entry.pack()

        # Campo de texto para Fecha (YYYY-MM-DD HH:MM)
        fecha_label = tk.Label(self.content, text="Fecha (YYYY-MM-DD HH:MM)")
        fecha_label.pack(pady=(10, 0))
        fecha_entry = tk.Entry(self.content)
        fecha_entry.pack()

        # Campo de texto para Trabajador ID
        trabajador_id_label = tk.Label(self.content, text="ID del Trabajador")
        trabajador_id_label.pack(pady=(10, 0))
        trabajador_id_entry = tk.Entry(self.content)
        trabajador_id_entry.pack()

        url = "http://127.0.0.1:8000/reservas"

        # Botón para enviar los datos
        submit_button = tk.Button(
            self.content,
            text="Registrar Reserva",
            command=lambda: self.cargar_datos_api2(
                url,
                cliente_id_entry.get(),
                servicio_id_entry.get(),
                fecha_entry.get(),
                trabajador_id_entry.get()
            )
        )
        submit_button.pack(pady=20)

    def cargar_datos_api2(self, url, cliente_id, servicio_id, fecha, trabajador_id):
        try:
            cliente_id = int(cliente_id)
            servicio_id = int(servicio_id)
            trabajador_id = int(trabajador_id)
            fecha = datetime.datetime.strptime(fecha, "%Y-%m-%d %H:%M")
            payload = {
                "cliente_id": cliente_id,
                "servicio_id": servicio_id,
                "fecha": fecha.isoformat(),
                "trabajador_id": trabajador_id
            }
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                messagebox.showinfo("Éxito", "Reserva creada correctamente.")
            else:
                messagebox.showerror(
                    "Error",
                    f"Error al crear reserva: {response.status_code} - {response.json().get('detail', 'No especificado')}"
                )
        except ValueError as e:
            messagebox.showerror("Error de tipo de datos", f"Por favor verifica los valores ingresados. Error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un problema al conectar con la API: {e}")

    def obtener_cliente_id(self, email):
        url = f"http://127.0.0.1:8000/clienteID/{email}"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                cliente_id = int(response.text.strip())
                return cliente_id
            except ValueError:
                print("Error: La respuesta de la API no es un número entero válido.")
                return None

    def crear_empleado(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        # Título de la sección
        empleado_label = tk.Label(self.content, text="Crear Empleado", font=("Arial", 20))
        empleado_label.pack(pady=20)

        # Campo de texto para Nombre
        nombre_label = tk.Label(self.content, text="Nombre")
        nombre_label.pack(pady=(10, 0))
        nombre_entry = tk.Entry(self.content)
        nombre_entry.pack()

        # Campo de texto para Email
        email_label = tk.Label(self.content, text="Email")
        email_label.pack(pady=(10, 0))
        email_entry = tk.Entry(self.content)
        email_entry.pack()

        # Campo de texto para Contraseña
        password_label = tk.Label(self.content, text="Contraseña")
        password_label.pack(pady=(10, 0))
        password_entry = tk.Entry(self.content, show="*")
        password_entry.pack()

        # Campo de texto para Rol
        rol_label = tk.Label(self.content, text="Rol")
        rol_label.pack(pady=(10, 0))
        rol_var = tk.StringVar()
        rol_combobox = ttk.Combobox(self.content, textvariable=rol_var)
        rol_combobox['values'] = ("Doctora", "Profesional", "Secretaria")
        rol_combobox.pack()

        url = "http://127.0.0.1:8000/workers/"

        # Botón para enviar los datos
        submit_button = tk.Button(
            self.content,
            text="Registrar Empleado",
            command=lambda: self.cargar_datos_api(
                url,
                nombre_entry.get(),
                email_entry.get(),
                password_entry.get(),
                rol_var.get()
            )
        )
        submit_button.pack(pady=20)

    def cargar_datos_api(self, url, nombre, email, password, rol):
        payload = {
            "nombre": nombre,
            "email": email,
            "password": password,
            "rol": rol
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code in [200, 201]:
                messagebox.showinfo("Éxito", "Empleado creado correctamente.")
            else:
                error_msg = response.json().get('detail', 'No especificado')
                messagebox.showerror("Error", f"Error al crear empleado: {response.status_code} - {error_msg}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Hubo un problema al conectar con la API: {e}")

    def listado_clientes(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        clientes_label = tk.Label(self.content, text="Listado de Clientes", font=("Arial", 20))
        clientes_label.pack(pady=1)

        encabezados = ["ID Cliente", "Nombre", "email", "Telefono"]
        campos = ["id", "nombre", "email", "telefono"]

        url = "http://127.0.0.1:8000/clientsg/"
        self.mostrar_datos_api(url, encabezados, campos)

    def listado_clientes_dia(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        clientes_dia_label = tk.Label(self.content, text="Listado de Clientes a Atender por Día", font=("Arial", 20))
        clientes_dia_label.pack(pady=1)

        # Campo de fecha de inicio
        self.fecha_label = tk.Label(self.content, text="Fecha de Inicio (aaaa-mm-dd):", font=("Arial", 14))
        self.fecha_label.pack(pady=5)
        self.fecha_entry = tk.Entry(self.content, font=("Arial", 14))
        self.fecha_entry.pack(pady=5)

        # Botón para buscar con la fecha ingresada
        btn_buscar = tk.Button(self.content, text="Buscar", font=("Arial", 14), command=self.buscar_clientes_dia)
        btn_buscar.pack(pady=10)

    def buscar_clientes_dia(self):
        fecha = self.fecha_entry.get()
        if not fecha:
            messagebox.showerror("Error", "Por favor ingrese una fecha.")
            return
        url = f"http://127.0.0.1:8000/reservasf/{fecha}"
        encabezados = ["Cliente", "Servicio", "Trabajador", "Fecha"]
        campos = ["cliente", "servicio", "trabajador", "fecha"]
        self.mostrar_datos_api(url, encabezados, campos)

    def ingresos_rango_fecha(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        ingresos_label = tk.Label(self.content, text="Ingresos en un Rango de Fecha", font=("Arial", 20))
        ingresos_label.pack(pady=1)

        self.fecha_inicio_label = tk.Label(self.content, text="Ingresar Fecha inicio:", font=("Arial", 14))
        self.fecha_inicio_label.pack(pady=5)
        self.fecha_inicio_entry = tk.Entry(self.content, font=("Arial", 14))
        self.fecha_inicio_entry.pack(pady=5)

        self.fecha_fin_label = tk.Label(self.content, text="Ingresar Fecha fin:", font=("Arial", 14))
        self.fecha_fin_label.pack(pady=5)
        self.fecha_fin_entry = tk.Entry(self.content, font=("Arial", 14))
        self.fecha_fin_entry.pack(pady=5)

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

    def administrar_profesionales(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        profesionales_label = tk.Label(self.content, text="Administrar Profesionales", font=("Arial", 20))
        profesionales_label.pack(pady=20)

        rango_fecha_label = tk.Label(
            self.content, text="Buscar Profesionales por Rango de Fecha", font=("Arial", 20)
        )
        rango_fecha_label.pack(pady=20)

        self.professional_id_label = tk.Label(
            self.content, text="Ingresar ID del Profesional:", font=("Arial", 14)
        )
        self.professional_id_label.pack(pady=5)
        self.professional_id_entry = tk.Entry(self.content, font=("Arial", 14))
        self.professional_id_entry.pack(pady=5)

        self.fecha_inicio_label = tk.Label(
            self.content, text="Fecha de Inicio (aaaa-mm-dd):", font=("Arial", 14)
        )
        self.fecha_inicio_label.pack(pady=5)
        self.fecha_inicio_entry = tk.Entry(self.content, font=("Arial", 14))
        self.fecha_inicio_entry.pack(pady=5)

        self.fecha_fin_label = tk.Label(
            self.content, text="Fecha de Fin (aaaa-mm-dd):", font=("Arial", 14)
        )
        self.fecha_fin_label.pack(pady=5)
        self.fecha_fin_entry = tk.Entry(self.content, font=("Arial", 14))
        self.fecha_fin_entry.pack(pady=5)

        self.btn_buscar = tk.Button(
            self.content, text="Buscar", font=("Arial", 14), command=self.mostrar_profesionales_por_fecha
        )
        self.btn_buscar.pack(pady=20)

    def mostrar_profesionales_por_fecha(self):
        trabajador_id = self.professional_id_entry.get()
        fecha_inicio = self.fecha_inicio_entry.get()
        fecha_fin = self.fecha_fin_entry.get()
        if not fecha_inicio or not fecha_fin or not trabajador_id:
            messagebox.showerror("Error", "Por favor ingrese ambas fechas y seleccione un profesional.")
            return
        encabezados = ["Cliente", "Servicio", "Trabajador", "Fecha"]
        campos = ["cliente", "Servicio", "Trabajador", "fecha"]
        url = f"http://127.0.0.1:8000/reservas/profesional/{fecha_inicio}/{fecha_fin}/{trabajador_id}"
        self.mostrar_datos_api(url, encabezados, campos)

    def atras(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        self.content.destroy()
        self.content = tk.Frame(self.root)
        self.content.pack(side="left", fill="both", expand=False)

    def generar_pago(self):
        # Limpiar el contenido anterior
        for widget in self.content.winfo_children():
            widget.destroy()

        # Título del formulario
        pago_label = tk.Label(self.content, text="Generar Pago", font=("Arial", 20))
        pago_label.grid(row=0, column=0, columnspan=4, pady=10)

        # Información del Cliente
        cliente_label = tk.Label(self.content, text="Información del Cliente", font=("Arial", 16))
        cliente_label.grid(row=1, column=0, columnspan=2, pady=5, sticky="w")

        # Email del Cliente
        email_label = tk.Label(self.content, text="Email:")
        email_label.grid(row=3, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(self.content)
        self.email_entry.grid(row=4, column=0, padx=5, pady=5)

        # Botón para buscar el cliente
        submit_button = tk.Button(self.content, text="Buscar Cliente", command=self.buscar_cliente)
        submit_button.grid(row=10, column=0, columnspan=4, pady=20)

    def buscar_cliente(self):
        self.cliente_email = self.email_entry.get()
        cliente_id_url = f"http://127.0.0.1:8000/clients/email/{self.cliente_email}"
        response = requests.get(cliente_id_url)
        if response.status_code == 200:
            self.cliente_res = response.json()
            self.mostrar_formulario_pago()
        else:
            print("Error: No se encontró el cliente con el email proporcionado.")

    def mostrar_datos_api5(self, url, encabezados, campos):
        try:
            response = requests.get(url)
            data_list = response.json()
            if isinstance(data_list, dict) and "error" in data_list:
                messagebox.showerror("Error", data_list["error"])
                return
            for i, encabezado in enumerate(encabezados):
                header_label = tk.Label(
                    self.content, text=encabezado, bg="green", fg="white", font=("Arial", 10, "bold")
                )
                header_label.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
            for row_index, data in enumerate(data_list, start=1):
                for col_index, campo in enumerate(campos):
                    value = data.get(campo, "N/A")
                    data_label = tk.Label(self.content, text=value)
                    data_label.grid(row=row_index, column=col_index, padx=5, pady=5)
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un problema al conectar con la API: {e}")

    def mostrar_formulario_pago(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        # Encabezados de tabla
        encabezados = ["Cliente", "Reserva", "Servicio", "Fecha reserva", "Monto total", "Abonado"]
        campos = ["Cliente", "Reserva", "Servicio", "Fecha reserva", "Monto total", "Abonado"]

        # Llamada a la API para mostrar encabezado y datos de la reserva
        url = f"http://127.0.0.1:8000/clients/email/{self.cliente_email}"
        self.mostrar_datos_api5(url, encabezados, campos)

        # Información de la Reserva
        reserva_label = tk.Label(self.content, text="Información de la Reserva", font=("Arial", 23))
        reserva_label.grid(row=16, column=1, columnspan=3, padx=2, pady=10, sticky="w")

        # Campo de entrada para ID de reserva
        id_reserva_label = tk.Label(self.content, text="Ingresar ID de la Reserva:", font=("Arial", 13))
        id_reserva_label.grid(row=18, column=1, padx=2, pady=1, sticky="e")
        self.id_reserva_entry = tk.Entry(self.content, width=20)
        self.id_reserva_entry.grid(row=18, column=2, padx=25, pady=1, sticky="w")

        # Botón para buscar la reserva
        reserva_button = tk.Button(
            self.content, text="Buscar Reserva", command=self.buscar_reserva,
            font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", relief="raised"
        )
        reserva_button.grid(row=20, column=1, padx=(10, 5), pady=5, ipadx=10, sticky="ew")

    def buscar_reserva(self):
        self.reserva_id = self.id_reserva_entry.get()
        self.mostrar_formulario_datos_pago()

    def mostrar_formulario_datos_pago(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        # Información del Pago
        pago_info_label = tk.Label(self.content, text="Información del Pago:", font=("Arial", 18, "bold"))
        pago_info_label.grid(row=1, column=0, columnspan=2, padx=5, sticky="w")

        # Monto
        monto_label = tk.Label(self.content, text="Monto:")
        monto_label.grid(row=2, column=0, padx=5, pady=5)
        self.monto_entry = tk.Entry(self.content)
        self.monto_entry.grid(row=3, column=0, padx=5, pady=5)

        # Método de Pago
        metodo_pago_label = tk.Label(self.content, text="Método de Pago:")
        metodo_pago_label.grid(row=4, column=0, padx=5, pady=5)

        # Menú desplegable para Método de Pago
        self.metodo_pago_var = tk.StringVar()
        metodo_pago_combobox = ttk.Combobox(self.content, textvariable=self.metodo_pago_var)
        metodo_pago_combobox['values'] = ("Efectivo", "Transferencia Bancaria", "Tarjeta de Crédito", "Tarjeta de Débito")
        metodo_pago_combobox.grid(row=5, column=0, padx=5, pady=5)

        # Botón para guardar el pago
        guardar_button = tk.Button(self.content, text="Guardar Pago", command=self.guardar_pago)
        guardar_button.grid(row=6, column=0, columnspan=2, pady=20)

    def guardar_pago(self):
        cliente_id = self.obtener_cliente_id(self.cliente_email)
        if cliente_id is None:
            print("Error: No se pudo obtener el ID del cliente.")
            return
        try:
            monto = float(self.monto_entry.get())
        except ValueError:
            print("Error: Monto debe ser un número válido.")
            return
        metodo_pago = self.metodo_pago_var.get()
        if metodo_pago not in ["Efectivo", "Transferencia Bancaria", "Tarjeta de Crédito", "Tarjeta de Débito"]:
            print("Error: Método de pago no válido.")
            return
        fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        payload = {
            "cliente_id": cliente_id,
            "monto": monto,
            "metodo_pago": metodo_pago,
            "fecha": fecha,
            "reserva_id": self.reserva_id
        }
        url = "http://127.0.0.1:8000/crearPago"
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Pago creado exitosamente")
            messagebox.showinfo("Éxito", "Pago creado correctamente.")
            self.mostrar_formulario_envio_factura()
        else:
            print(f"Error al crear el pago: {response.json()}")

    def mostrar_formulario_envio_factura(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        # Título para la sección de envío de factura
        factura_label = tk.Label(self.content, text="Enviar Factura", font=("Arial", 16))
        factura_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

        # Email para enviar la factura
        email_label = tk.Label(self.content, text="Correo electrónico:")
        email_label.grid(row=1, column=0, padx=5, pady=5)
        self.from_email_entry = tk.Entry(self.content)
        self.from_email_entry.grid(row=2, column=0, padx=5, pady=5)

        # Contraseña para el correo
        password_label = tk.Label(self.content, text="Contraseña del correo:")
        password_label.grid(row=3, column=0, padx=5, pady=5)
        self.from_password_entry = tk.Entry(self.content, show="*")
        self.from_password_entry.grid(row=4, column=0, padx=5, pady=5)

        # Botón para enviar la factura
        enviar_button = tk.Button(self.content, text="Enviar Factura", command=self.enviar_factura)
        enviar_button.grid(row=5, column=0, columnspan=2, pady=20)

    def enviar_factura(self):
        from_email = self.from_email_entry.get()
        from_password = self.from_password_entry.get()
        if not from_email or not from_password:
            messagebox.showerror("Error", "Credenciales de correo no ingresadas.")
            return
        self.enviar_factura_con_datos(self.cliente_email, self.reserva_id, from_email, from_password)

    def enviar_factura_con_datos(self, cliente_id, reserva_id, from_email, from_password):
        payload = {
            "reserva_id": reserva_id,
            "from_email": from_email,
            "from_password": from_password
        }
        url = f"http://127.0.0.1:8000/enviar_factura?reserva_id={reserva_id}"
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            messagebox.showinfo("Éxito", "Factura generada y enviada exitosamente.")
        else:
            error_msg = response.json().get("detail", "Error desconocido al enviar la factura")
            messagebox.showerror("Error", error_msg)

# Para ejecutar la ventana de secretaria
def mostrar_pagina_secretaria(token):
    root = tk.Tk()
    SecretariaPage(root, token)
    root.mainloop()
