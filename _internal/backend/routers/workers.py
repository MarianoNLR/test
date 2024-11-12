from fastapi import APIRouter, HTTPException
import crud
from auth import create_access_token
from models import Trabajador
from datetime import timedelta,datetime
import uvicorn

router = APIRouter()

@router.post("/workers/", response_model=dict)
def create_trabajador(trabajador: Trabajador):
    trabajador.password = trabajador.password
    return crud.create_trabajador(trabajador)

@router.post("/login/{email}/{password}")
def login(email: str, password: str):
    trabajador = crud.get_trabajador_by_email(email)
    if not trabajador or password != trabajador["password"]:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": trabajador["email"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/reservas/profesional/{fecha_inicio}/{fecha_fin}/{trabajador_id}")
def traer_servicios_xprofesional_porfecha(fecha_inicio:str,fecha_fin:str, trabajador_id:int):
    r = crud.get_reservas_por_profesional(fecha_inicio,fecha_fin,trabajador_id)
    return r
