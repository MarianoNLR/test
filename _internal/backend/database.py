# import pyodbc
# # Configuración de la cadena de conexión a SQL Server
# connection_string = (
#     "DRIVER={ODBC Driver 17 for SQL Server};"
#     "SERVER=DESKTOP-9EJJ77C;"
#     "DATABASE=spa_db;"
#     "UID=sa;"
#     "PWD=686050;"
# )

# # Crear la conexión a la base de datos
# def get_db_connection():
#     conn = pyodbc.connect(connection_string)
#     return conn

# # Función para ejecutar consultas de manera segura
# def execute_query(query, params=None):
#     conn = None
#     cursor = None
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
        
#         if params:
#             cursor.execute(query, params)
#         else:
#             cursor.execute(query)

#         # No necesitamos commit para SELECT
#         if query.strip().upper().startswith("SELECT"):
#             return cursor  # Retornar el cursor para lectura
        
#         # Si no es un SELECT, realizamos commit
#         conn.commit()
#         return cursor

#     except pyodbc.Error as ex:
#         print("Error durante la ejecución de la consulta:", ex)
#         return None

#     finally:
#         # Cerramos el cursor y la conexión
#         if cursor:
#             cursor.close()
#         if conn:
#             conn.close()
import sqlite3

# Configuración de la base de datos SQLite
DATABASE_PATH = "spa_db.sqlite"  # Asegúrate de que la ruta sea correcta

# Crear la conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    return conn

# Función para ejecutar consultas de manera segura
def execute_query(query, params=None):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        # No necesitamos commit para SELECT
        if query.strip().upper().startswith("SELECT"):
            return cursor.fetchall()  # Retorna los resultados de la consulta como lista de tuplas
        
        # Si no es un SELECT, realizamos commit
        conn.commit()
        return cursor.lastrowid  # Retorna el ID del último registro insertado, útil para INSERT

    except sqlite3.Error as ex:
        print("Error durante la ejecución de la consulta:", ex)
        return None

    finally:
        # Cerramos el cursor y la conexión
        if cursor:
            cursor.close()
        if conn:
            conn.close()
