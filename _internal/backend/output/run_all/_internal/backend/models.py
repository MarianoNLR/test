from enum import Enum
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uvicorn

class Role(str, Enum):
    """Clase Roles"""
    doctora = "Doctora"
    profesional = "Profesional"
    secretaria = "Secretaria"
    cliente = "cliente"

class metodosPago(str, Enum):
    """Clase Metodos de pago"""
    efectivo = "Efectivo"
    transferencia = "Transferencia Bancaria"
    credito = "Tarjeta de Crédito"
    debito = "Tarjeta de Débito"
    
class Servicio(BaseModel):
    """Clase Servicio"""
    id: Optional[int] = None
    nombre: str
    descripcion: str
    precio: float

class Reserva(BaseModel):
    """Clase Reserva"""
    id: Optional[int] = None
    cliente_id: int
    servicio_id: int
    fecha: datetime
    trabajador_id: int

class Pago(BaseModel):
    """Clase Pago"""
    id: Optional[int] = None
    cliente_id: int
    monto: float
    metodo_pago: metodosPago
    fecha: datetime
    reserva_id: int

class Trabajador(BaseModel):
    """Clase Trabajador"""
    id: Optional[int] = None
    nombre: str
    email: str
    password: str
    rol: Role

class Cliente(Trabajador):
    """Clase cliente"""
    telefono: str

class EmailCredentials(BaseModel):
    from_email: str
    from_password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class Reserva2(BaseModel):
    """Clase Reserva"""
    id: Optional[int] = None
    servicio_id: int
    fecha: datetime
    trabajador_id: int

