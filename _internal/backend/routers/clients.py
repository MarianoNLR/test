from database import execute_query, get_db_connection
from fastapi import APIRouter, HTTPException
from crud import *
from models import *
from auth import *

class CredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error en las credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )

router = APIRouter()
class Requests:
    @router.post("/clients/", response_model=dict)
    def create_client(cliente: Cliente):
        cliente.password = cliente.password
        return create_client(cliente)
    @router.get("/clientsg/")
    def get_clients():
        return get_clients()
    @router.get("/clients/{cliente_id}")
    def get_client():
        return get_cliente_by_id(cliente_id=int)
    @router.get("/clients/xday_and_services")
    def get_clients_xday_and_services():
        return get_clients_xday_and_services()

    @router.get("/clients/xprofesional_byHours")
    def get_clients_xprofesional_byHours():
        return get_clients_xprofesional_byHours()

    @router.post("/auth/login")
    def authenticate_client(login_request: LoginRequest):
        email = login_request.email
        password = login_request.password
        print('xd', email, password)
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Consulta adaptada para SQLite
            query = """
            SELECT id, nombre, email, password, rol FROM Clientes WHERE email = ?
            UNION
            SELECT id, nombre, email, password, rol FROM Trabajadores WHERE email = ?
            """
            cursor.execute(query, (email, email))
            client = cursor.fetchone()
            print(client)
            # Verificación de credenciales
            if client is None or password != client[3]:
                raise CredentialsException()

            # Crear token de acceso
            access_token = create_access_token(data={"sub": email, "id": client[0], "rol": client[4]})
            print(access_token)
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "id": client[0],
                "nombre": client[1],
                "email": client[2],
                "rol": client[4]
            }
        except CredentialsException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        # Endpoint para la autenticación
    # @router.post("/auth/login")
    # def authenticate_client(login_request: LoginRequest):
    #     email = login_request.email
    #     password = login_request.password

    #     try:
    #         conn = get_db_connection()
    #         cursor = conn.cursor()
    #         query = """
    #         SELECT id, nombre, email, password, rol FROM Clientes WHERE email = ?
    #         UNION
    #         SELECT id, nombre, email, password, rol FROM Trabajadores WHERE email = ?
    #         """
    #         cursor.execute(query, (email, email))
    #         client = cursor.fetchone()

    #         if client is None or password != client[3]:
    #             raise CredentialsException()

    #         # Crear token de acceso
    #         access_token = create_access_token(data={"sub": email, "id": client[0], "rol": client[4]})

    #         return {
    #             "access_token": access_token,
    #             "token_type": "bearer",
    #             "id": client[0],
    #             "nombre": client[1],
    #             "email": client[2],
    #             "rol": client[4]
    #         }
    #     except CredentialsException:
    #         raise
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=str(e))
    #     finally:
    #         if cursor:
    #             cursor.close()
    #         if conn:
    #             conn.close()
    
    @router.get("/clients/email/{email}")
    def clienteXMail(email:str):
        return get_cliente_by_email(email)
    @router.get("/clienteID/{email}", response_model=int)
    def clienteID(email: str):
        cliente_id = get_clienteid_by_email(email)
        if cliente_id is None:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return cliente_id