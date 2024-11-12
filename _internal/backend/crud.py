
import pyodbc
import sqlite3
from database import execute_query, get_db_connection
from models import *
from datetime import datetime
##############################INICIO#######################################
# Crear un cliente
def create_client(cliente: Cliente):
    try:
        query = """
        INSERT INTO Clientes (nombre, email, telefono, password, rol)
        VALUES (?, ?, ?, ?, ?);
        """
        execute_query(query, (cliente.nombre, cliente.email, cliente.telefono, cliente.password, cliente.rol))
        return {"message": "Cliente creado con éxito"}
    
    except sqlite3.Error as ex:
        print(f"Error durante la creación del cliente: {ex}")
        return {"error": "Error al crear el cliente. Verifica los datos e intente nuevamente."}

    except Exception as ex:
        print(f"Error inesperado: {ex}")
        return {"error": "Se produjo un error inesperado. Contacte al soporte."}

# Actualizar un cliente
def update_client(cliente: Cliente):
    try:
        query = """
        UPDATE Clientes
        SET nombre = ?, email = ?, telefono = ?, password = ?
        WHERE id = ?;
        """
        execute_query(query, (cliente.nombre, cliente.email, cliente.telefono, cliente.password, cliente.id))
        return {"message": "Cliente actualizado con éxito"}

    except sqlite3.Error as ex:
        print(f"Error durante la actualización del cliente: {ex}")
        return {"error": "No se pudo actualizar el cliente. Verifica los datos e intenta nuevamente."}
    
    except Exception as ex:
        print(f"Error inesperado: {ex}")
        return {"error": "Ocurrió un error inesperado. Contacte al soporte técnico."}

# Obtener todos los clientes
def get_clients():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM Clientes"
        cursor.execute(query)
        rows = cursor.fetchall()
        clients = []
        for row in rows:
            clients.append({
                "id": row[0],
                "nombre": row[1],
                "email": row[2],
                "telefono": row[3]
            })
        return clients
    except sqlite3.Error as ex:
        print(f"Error al obtener clientes: {ex}")
        return {"error": "No se pudo obtener la lista de clientes. Intenta más tarde."}
    
    except Exception as ex:
        print(f"Error inesperado: {ex}")
        return {"error": "Ocurrió un error inesperado. Contacte al soporte técnico."}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Borrar cliente
def delete_client(cliente_id: int):
    try:
        query = "DELETE FROM Clientes WHERE id = ?;"
        execute_query(query, (cliente_id,))
        return {"message": "Cliente eliminado con éxito"}
    
    except sqlite3.Error as ex:
        print(f"Error al eliminar cliente: {ex}")
        return {"error": "No se pudo eliminar el cliente. Es posible que tenga reservas asociadas."}
    
    except Exception as ex:
        print(f"Error inesperado: {ex}")
        return {"error": "Ocurrió un error inesperado. Contacte al soporte técnico."}

# Crear trabajador
def create_trabajador(trabajador: Trabajador):
    """crear trabajador"""
    query = """
    INSERT INTO Trabajadores (nombre, email, password, rol)
    VALUES (?, ?, ?, ?);
    """
    execute_query(query, (trabajador.nombre, trabajador.email, trabajador.password, trabajador.rol))
    return {"message": "Trabajador creado con éxito"}

# Actualizar trabajador
def update_trabajador(trabajador: Trabajador):
    try:
        query = """
        UPDATE Trabajadores
        SET nombre = ?, email = ?, password = ?, rol = ?
        WHERE id = ?;
        """
        execute_query(query, (trabajador.nombre, trabajador.email, trabajador.password, trabajador.rol, trabajador.id))
        return {"message": "Trabajador actualizado con éxito"}

    except sqlite3.Error as ex:
        print(f"Error durante la actualización del trabajador: {ex}")
        return {"error": "No se pudo actualizar el trabajador. Verifica los datos e intenta nuevamente."}
    
    except Exception as ex:
        print(f"Error inesperado: {ex}")
        return {"error": "Ocurrió un error inesperado. Contacte al soporte técnico."}

# Borrar trabajador
def delete_trabajador(trabajador_id: int):
    try:
        query = "DELETE FROM Trabajadores WHERE id = ?;"
        execute_query(query, (trabajador_id,))
        return {"message": "Trabajador eliminado con éxito"}
    except sqlite3.Error as ex:
        print(f"Error al eliminar trabajador: {ex}")
        return {"error": "No se pudo eliminar el trabajador. Verifica los datos e intenta nuevamente."} 
    except Exception as ex:
        print(f"Error inesperado: {ex}")
        return {"error": "Ocurrió un error inesperado. Contacte al soporte técnico."}


# Obtener cliente por email
def get_cliente_by_email(email: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """         
            SELECT 
            c.nombre AS Cliente, 
            r.id AS Reserva, 
            s.nombre AS Servicio,  
            r.fecha AS 'Fecha reserva', 
            s.precio AS 'Monto total',
            COALESCE(p.monto, 0) AS Abonado
            FROM Clientes c
            JOIN Reservas r ON r.cliente_id = c.id
            JOIN Servicios s ON s.id = r.servicio_id
            LEFT JOIN Pagos p ON p.reserva_id = r.id
            WHERE c.email = ? 
            AND (p.monto IS NULL OR p.monto < s.precio) 
            ORDER BY r.fecha;
        """
        
        cursor.execute(query, (email,))
        rows = cursor.fetchall()
        
        clientslist = []
        for row in rows:
            clientslist.append({
                "Cliente": row[0],
                "Reserva": row[1],
                "Servicio": row[2],
                "Fecha reserva": row[3],
                "Monto total": row[4],
                "Abonado": row[5]
            })
        
        return clientslist
    except sqlite3.Error as ex:
        print(f"Error: {ex}")
        return {"error": "No se pudieron obtener las reservas."}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Obtener clientes por día y servicios
def get_clients_xday_and_services():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT 
            c.nombre AS Cliente, 
            s.nombre AS Servicio,
            date(r.fecha) AS Fecha,
            time(r.fecha) AS Hora
            FROM Clientes c
            JOIN Reservas r ON r.cliente_id = c.id
            JOIN Servicios s ON s.id = r.servicio_id
            ORDER BY r.fecha ASC;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        clientslist = []
        for row in rows:
            clientslist.append({
                "Cliente": row[0],
                "Servicio": row[1],
                "Fecha": row[2],
                "Hora": row[3]
            })
        return clientslist
    except sqlite3.Error as ex:
        print("Error:", ex)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Obtener clientes por profesional y por hora
def get_clients_xprofesional_byHours():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT 
            c.nombre AS Cliente, 
            t.nombre AS Profesional,
            date(r.fecha) AS Fecha,
            time(r.fecha) AS Hora
            FROM Clientes c
            JOIN Reservas r ON r.cliente_id = c.id
            JOIN Trabajadores t ON t.id = r.trabajador_id
            ORDER BY r.fecha ASC;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        clientslist = []
        for row in rows:
            clientslist.append({
                "Cliente": row[0],
                "Profesional": row[1],
                "Fecha": row[2],
                "Hora": row[3]
            })
        return clientslist
    except sqlite3.Error as ex:
        print("Error:", ex)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Obtener pagos por día
def get_Payments_xday():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        fechaInicio = '2024-10-20 00:00:00'
        fechaFin = '2024-10-29 00:00:00'
        query = """
            SELECT *
            FROM Pagos
            WHERE fecha >= ? AND fecha <= ?;
        """
        cursor.execute(query, (fechaInicio, fechaFin))
        rows = cursor.fetchall()

        pagoslist = []
        for row in rows:
            pagoslist.append({
                "id": row[0],
                "cliente_id": row[1],
                "monto": row[2],
                "metodo_pago": row[3],
                "fecha": row[4],
                "reserva_id": row[5]
            })
        return pagoslist
    except sqlite3.Error as ex:
        print("Error durante la ejecución de la consulta:", ex)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Crear una reserva
def create_reserva(reserva: Reserva):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO Reservas (cliente_id, servicio_id, fecha, trabajador_id)
        VALUES (?, ?, ?, ?);
        """
        execute_query(query, (reserva.cliente_id, reserva.servicio_id, reserva.fecha, reserva.trabajador_id))
        return {"message": "Reserva creada con éxito"}
    except sqlite3.Error as ex:
        print(f"Error al crear la reserva: {ex}")
        return {"error": "No se pudo crear la reserva. Verifica los datos e intenta nuevamente."}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Crear reserva WEB
def create_reserva2(reserva: Reserva2, cliente_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO Reservas (cliente_id, servicio_id, fecha, trabajador_id)
        VALUES (?, ?, ?, ?);
        """
        print(reserva.trabajador_id)
        execute_query(query, (cliente_id, reserva.servicio_id, reserva.fecha, reserva.trabajador_id))
        return {"message": "Reserva creada con éxito"}
    except sqlite3.Error as ex:
        print(f"Error al crear la reserva: {ex}")
        return {"error": "No se pudo crear la reserva. Verifica los datos e intenta nuevamente."}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Obtener todas las reservas
def get_todas_las_reservas():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT c.nombre AS Cliente, s.nombre AS Servicio, t.nombre AS Trabajador, r.fecha
            FROM Reservas r
            JOIN Clientes c ON c.id = r.cliente_id
            JOIN Servicios s ON s.id = r.servicio_id
            JOIN Trabajadores t ON t.id = r.trabajador_id;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        reservas = []
        for row in rows:
            reservas.append({
                "Cliente": row[0],
                "Servicio": row[1],
                "Trabajador": row[2],
                "fecha": row[3],
            })
        return reservas  
    except sqlite3.Error as ex:
        print(f"Error al obtener las reservas: {ex}")
        return {"error": "No se pudieron obtener las reservas."}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Traer todas las reservas del día
def get_reservas_del_dia():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        fecha_hoy = datetime.now().strftime('%Y-%m-%d')
        query = """
            SELECT 
                c.nombre AS Cliente,
                s.nombre AS Servicio,
                t.nombre AS Trabajador,
                r.fecha
            FROM Reservas r
            JOIN Clientes c ON c.id = r.cliente_id
            JOIN Servicios s ON s.id = r.servicio_id
            JOIN Trabajadores t ON t.id = r.trabajador_id
            WHERE date(r.fecha) = ?;
        """
        cursor.execute(query, (fecha_hoy,))
        rows = cursor.fetchall()
        reservas = []
        for row in rows:
            reservas.append({
                "cliente": row[0],
                "servicio": row[1],
                "trabajador": row[2],
                "fecha": row[3]
            })
        return reservas  
    except sqlite3.Error as ex:
        print(f"Error al obtener las reservas del día: {ex}")
        return {"error": "No se pudieron obtener las reservas del día."}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Actualizar una reserva
def update_reserva(reserva: Reserva):
    try:
        query = """
        UPDATE Reservas
        SET cliente_id = ?, servicio_id = ?, fecha = ?, trabajador_id = ?
        WHERE id = ?;
        """
        execute_query(query, (reserva.cliente_id, reserva.servicio_id, reserva.fecha, reserva.trabajador_id, reserva.id))
        return {"message": "Reserva actualizada con éxito"}
    except sqlite3.Error as ex:
        print(f"Error al actualizar la reserva: {ex}")
        return {"error": "No se pudo actualizar la reserva. Verifica los datos e intenta nuevamente."}
    
# Eliminar una reserva
def delete_reserva(reserva_id: int):
    try:
        query = "DELETE FROM Reservas WHERE id = ?;"
        execute_query(query, (reserva_id,))
        return {"message": "Reserva eliminada con éxito"}
    except sqlite3.Error as ex:
        print(f"Error durante la eliminación de la reserva: {ex}")
        return {"error": "No se pudo eliminar el trabajador. Verifica los datos e intenta nuevamente."} 
    except Exception as ex:
        print(f"Error inesperado: {ex}")
        return {"error": "Ocurrió un error inesperado. Contacte al soporte técnico."}

# Traer cliente por ID
def get_cliente_by_id(cliente_id: int):
    try:
        query = "SELECT * FROM Clientes WHERE id = ?;"
        cursor = execute_query(query, (cliente_id,))
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "nombre": row[1],
                "email": row[2],
                "telefono": row[3]
            }
        return None
    except sqlite3.Error as ex:
        print(f"Error durante la obtención del cliente: {ex}")
        return {"error": "No se pudo obtener el cliente. Verifica los datos e intenta nuevamente."} 
    except Exception as ex:
        print(f"Error inesperado: {ex}")
        return {"error": "Ocurrió un error inesperado. Contacte al soporte técnico."}

# Traer trabajador por ID
def get_trabajador_by_id(trabajador_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM Trabajadores WHERE id = ?;"
        cursor = execute_query(query, (trabajador_id,))
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "nombre": row[1],
                "email": row[2],
                "password": row[3],
                "rol": row[4]
            }
        return None
    except sqlite3.Error as ex:
        print(f"Error durante la obtención del trabajador: {ex}")
        return {"error": "No se pudo obtener el trabajador. Verifica los datos e intenta nuevamente."} 
    except Exception as ex:
        print(f"Error inesperado: {ex}")
        return {"error": "Ocurrió un error inesperado. Contacte al soporte técnico."}

# Traer reservas por fecha
def get_reservas_por_fecha(fecha: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                c.nombre AS Cliente,
                s.nombre AS Servicio,
                t.nombre AS Trabajador,
                r.fecha
            FROM Reservas r
            JOIN Clientes c ON c.id = r.cliente_id
            JOIN Servicios s ON s.id = r.servicio_id
            JOIN Trabajadores t ON t.id = r.trabajador_id
            WHERE date(r.fecha) = ?;
        """
        cursor.execute(query, (fecha,))
        rows = cursor.fetchall()
        reservas = []
        for row in rows:
            reservas.append({
                "cliente": row[0],
                "servicio": row[1],
                "trabajador": row[2],
                "fecha": row[3]
            })
        return reservas  
    except sqlite3.Error as ex:
        print(f"Error al obtener las reservas por fecha: {ex}")
        return {"error": "No se pudieron obtener las reservas para la fecha especificada."}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Traer reservas por cliente ID
def get_reservas_by_cliente(cliente_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT 
                r.id,
                c.nombre AS Cliente,
                s.nombre AS Servicio,
                r.fecha,
                t.nombre AS Trabajador
            FROM Reservas r
            JOIN Clientes c ON r.cliente_id = c.id
            JOIN Servicios s ON r.servicio_id = s.id
            JOIN Trabajadores t ON r.trabajador_id = t.id
            WHERE r.cliente_id = ?;
        """
        cursor.execute(query, (cliente_id,))
        rows = cursor.fetchall()
        reservas = []
        for row in rows:
            reservas.append({
                "reserva_id": row[0],
                "cliente_id": row[1],
                "servicio_id": row[2],
                "fecha": row[3],
                "trabajador_id": row[4]
            })
        return reservas
    except sqlite3.Error as ex:
        print(f"Error durante la obtención de las reservas: {ex}")
        return {"error": "Error durante la obtención de las reservas."} 
    except Exception as ex:
        print(f"Error inesperado: {ex}")
        return {"error": "Ocurrió un error inesperado. Contacte al soporte técnico."}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Crear un pago
def create_pago(pago: Pago):
    try:
        query = """
        INSERT INTO Pagos (cliente_id, monto, metodo_pago, fecha, reserva_id)
        VALUES (?, ?, ?, ?, ?);
        """
        execute_query(query, (pago.cliente_id, pago.monto, pago.metodo_pago, pago.fecha, pago.reserva_id))
        return {"message": "Pago creado con éxito"}
    except sqlite3.Error as ex:
        print(f"Error durante la creación del pago: {ex}")
        return {"error": "No se pudo crear el pago. Verifica los datos e intenta nuevamente."} 
    except Exception as ex:
        print(f"Error inesperado: {ex}")
        return {"error": "Ocurrió un error inesperado. Contacte al soporte técnico."}

# Obtener servicios disponibles
def get_servicios_disponibles():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT DISTINCT(nombre) FROM Servicios"
        cursor.execute(query)
        rows = cursor.fetchall()
        servicios = [row[0] for row in rows]
        return servicios  
    except sqlite3.Error as ex:
        print(f"Error al obtener los servicios: {ex}")
        return {"error": "No se pudo obtener la lista de servicios."}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Obtener ID de cliente por email
def get_clienteid_by_email(email: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        consulta = "SELECT id FROM Clientes WHERE email = ?"
        cursor.execute(consulta, (email,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        else:
            return None
    except sqlite3.Error as ex:
        print(f"Error al obtener el ID: {ex}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Obtener datos de factura
def obtener_datos_factura(reserva_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        consulta = """
            SELECT 
                c.nombre AS Cliente, 
                c.email AS Email,
                c.telefono AS Telefono, 
                s.nombre AS Servicio, 
                s.descripcion AS Descripcion, 
                r.fecha AS FechaReserva, 
                s.precio AS PrecioServicio,
                p.monto AS TotalAbonado,
                p.metodo_pago AS MetodoPago,
                p.fecha AS FechaPago
            FROM Clientes c
            JOIN Reservas r ON r.cliente_id = c.id
            JOIN Servicios s ON s.id = r.servicio_id
            LEFT JOIN Pagos p ON p.reserva_id = r.id
            WHERE r.id = ?
        """
        cursor.execute(consulta, (reserva_id,))
        resultado = cursor.fetchone()

        if resultado:
            return {
                "cliente": {
                    "nombre": resultado[0],
                    "email": resultado[1],
                    "telefono": resultado[2]
                },
                "servicio": {
                    "nombre": resultado[3],
                    "descripcion": resultado[4],
                    "precio": resultado[5]
                },
                "reserva": {
                    "fecha": resultado[6]
                },
                "pago": {
                    "monto": resultado[7],
                    "metodo_pago": resultado[8],
                    "fecha": resultado[9]
                }
            }
        else:
            return None
    except sqlite3.Error as e:
        print(f"Error al obtener los datos de la factura: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Obtener ingresos por tipo de pago
def get_ingresos_por_tipo_de_pago(fecha_inicio: str, fecha_fin: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        consulta = """
        SELECT metodo_pago, SUM(monto) AS total_ingresos
        FROM Pagos
        WHERE fecha BETWEEN ? AND ?
        GROUP BY metodo_pago;
        """
        cursor.execute(consulta, (fecha_inicio, fecha_fin))
        return cursor.fetchall()
    except sqlite3.Error as ex:
        print(f"Error al obtener ingresos: {ex}")
        return {"error": "Error al obtener los datos de ingresos"}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Obtener reserva por ID
def get_reserva_by_id(reserva_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM Reservas WHERE id = ?"
        cursor.execute(query, (reserva_id,))
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "cliente_id": row[1],
                "servicio_id": row[2],
                "fecha": row[3],
                "trabajador_id": row[4]
            }
        return None
    except sqlite3.Error as ex:
        print(f"Error al obtener la reserva: {ex}")
        return {"error": "Error al obtener los datos de la reserva, consulte con soporte técnico"}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Obtener servicio por ID
def get_servicio_by_id(servicio_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM Servicios WHERE id = ?"
        cursor.execute(query, (servicio_id,))
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "nombre": row[1],
                "descripcion": row[2],
                "precio": row[3]
            }
        return None
    except sqlite3.Error as ex:
        print(f"Error al obtener el servicio: {ex}")
        return {"error": "Error al obtener los datos del servicio"}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Obtener reservas por profesional en un rango de fechas
def get_reservas_por_profesional(fecha_inicio: str, fecha_fin: str, trabajador_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT c.nombre AS Cliente, s.nombre AS Servicio, t.nombre AS Trabajador, r.fecha 
            FROM Reservas r
            JOIN Clientes c ON c.id = r.cliente_id
            JOIN Trabajadores t ON t.id = r.trabajador_id
            JOIN Servicios s ON s.id = r.servicio_id
            WHERE r.fecha BETWEEN ? AND ? AND t.id = ?
        """
        cursor.execute(query, (fecha_inicio, fecha_fin, trabajador_id))
        rows = cursor.fetchall()
        reservas = []
        for row in rows:
            reservas.append({
                "cliente": row[0],
                "servicio": row[1],
                "trabajador": row[2],
                "fecha": row[3],
            })
        return reservas
    except sqlite3.Error as ex:
        print(f"Error al obtener las reservas: {ex}")
        return {"error": "No se pudieron obtener las reservas."}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Autenticar cliente o trabajador
def authenticate_client(email: str, password: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT id, nombre, email, rol FROM Clientes WHERE email = ? AND password = ?
            UNION
            SELECT id, nombre, email, rol FROM Trabajadores WHERE email = ? AND password = ?
        """
        cursor.execute(query, (email, password, email, password))
        client = cursor.fetchone()
        if client:
            return {
                "id": client[0],
                "nombre": client[1],
                "email": client[2],
                "rol": client[3]
            }
        return None
    except sqlite3.Error as ex:
        print(f"Error en la autenticación: {ex}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Obtener todos los trabajadores
def get_todos_los_trabajadores():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM Trabajadores;"
        cursor.execute(query)
        rows = cursor.fetchall()

        trabajadores = []
        for row in rows:
            trabajadores.append({
                "id": row[0],
                "nombre": row[1],
                "email": row[2],
                "password": row[3],  # Recuerda que no deberías enviar la contraseña en respuestas normales
                "rol": row[4]
            })

        return trabajadores
    except sqlite3.Error as ex:
        print(f"Error al obtener los trabajadores: {ex}")
        return {"error": "No se pudieron obtener los trabajadores."}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Obtener trabajador por email
def get_trabajador_by_email(email: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM Trabajadores WHERE email = ?"
        cursor.execute(query, (email,))
        trabajador = cursor.fetchone()
        if trabajador:
            return {
                "id": trabajador[0],
                "email": trabajador[1],
                "nombre": trabajador[2],
                "password": trabajador[3]
            }
        return None
    except sqlite3.Error as ex:
        print(f"Error al obtener el trabajador: {ex}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Obtener servicios por profesional en un rango de fechas
def get_servicios_por_profesional(fecha_inicio: str, fecha_fin: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        consulta = """
            SELECT t.nombre AS profesional, s.nombre AS servicio, r.fecha
            FROM Reservas r
            JOIN Trabajadores t ON r.trabajador_id = t.id
            JOIN Servicios s ON r.servicio_id = s.id
            WHERE r.fecha BETWEEN ? AND ?
            ORDER BY t.nombre, r.fecha;
        """
        cursor.execute(consulta, (fecha_inicio, fecha_fin))
        rows = cursor.fetchall()
        
        servicios = []
        for row in rows:
            servicios.append({
                "profesional": row[0],
                "servicio": row[1],
                "fecha": row[2]
            })

        return servicios
    except sqlite3.Error as ex:
        print(f"Error al obtener los servicios: {ex}")
        return {"error": "Error al obtener los datos de servicios"}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()