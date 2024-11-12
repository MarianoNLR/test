from fastapi import APIRouter, Query
from fastapi.responses import FileResponse
from crud import get_ingresos_por_tipo_de_pago, get_servicios_por_profesional
from utils import generar_el_pdf_informe_ingresos,generar_pdf_informe_servicios
from fastapi import HTTPException
router = APIRouter()


# def generar_pdf2():
#     """texto"""
#     return FileResponse(generar_pdf)
# Endpoint para generar informe de ingresos por tipo de pago
@router.get("/informe/ingresos/{fecha_inicio}/{fecha_fin}")
def generar_pdf_informe_ingresos(fecha_inicio: str, fecha_fin: str):
    # Obtén los datos según el rango de fechas
    datos = get_ingresos_por_tipo_de_pago(fecha_inicio, fecha_fin)
    if "error" in datos:
        raise HTTPException(status_code=500, detail="Error al obtener los datos")

    # Llama a una función específica para generar el PDF
    nombre_archivo_pdf = generar_el_pdf_informe_ingresos(datos)
    
    return FileResponse(nombre_archivo_pdf, media_type='application/pdf', filename=nombre_archivo_pdf)


#Endpoint para generar informe de servicios por profesional
@router.get("/informe/servicios")
def generar_informe_servicios(fecha_inicio: str, fecha_fin: str):
    datos = get_servicios_por_profesional(fecha_inicio, fecha_fin)
    if "error" in datos:
        raise HTTPException(status_code=500, detail="Error al obtener los datos")
    
    nombre_archivo_pdf = generar_pdf_informe_servicios(datos)
    return FileResponse(nombre_archivo_pdf, media_type='application/pdf', filename=nombre_archivo_pdf)
