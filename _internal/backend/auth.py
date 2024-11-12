from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
import base64
import json
from database import *
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Configuración de expiración del token
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class credentials_exception(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error en las credenciales")

# Crear token de acceso sin encriptación
def create_access_token(data: dict, expires_delta: timedelta = None):
    print('xd', data)
    to_encode = data.copy()
    expire = (datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))).isoformat()
    to_encode.update({"exp": expire})
    # Convertir el diccionario a una cadena JSON y luego a base64
    token_str = json.dumps(to_encode)
    token_bytes = token_str.encode('utf-8')
    token_base64 = base64.b64encode(token_bytes).decode('utf-8')
    return token_base64

def decode_access_token(token: str):
    try:
        token_bytes = base64.b64decode(token.encode('utf-8'))
        token_str = token_bytes.decode('utf-8')
        data = json.loads(token_str)
        return data  # Esto devuelve el contenido decodificado del token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )

# Obtener usuario actual sin desencriptación
def get_current_user(token: str):
    try:
        # Decodificar el token de base64 a cadena JSON
        token_bytes = base64.b64decode(token.encode('utf-8'))
        token_str = token_bytes.decode('utf-8')
        data = json.loads(token_str)
        email = data.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except Exception as exc:
        raise credentials_exception from exc


def get_current_cliente_id(token: str = Depends(oauth2_scheme)):
    data = decode_access_token(token)
    cliente_id = data.get("id")
    if cliente_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo obtener el ID del cliente"
        )
    return cliente_id