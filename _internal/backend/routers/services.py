from fastapi import APIRouter, Depends
from crud import *
import uvicorn

router = APIRouter()

@router.get("/servicios")
async def obtener_servicios():
    servicios = get_servicios_disponibles()
    if "error" in servicios:
        return {"error": servicios["error"]}
    return servicios
