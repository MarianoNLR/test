"""importaciones"""
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from fastapi import APIRouter, Body, HTTPException
import crud
from models import *
from emails_senders import *

router = APIRouter()
# Función para generar factura en PDF usando ReportLab
def generar_factura_pdf(cliente, pago, reserva, servicio):
    try:
        nombre_archivo = f"factura_{cliente['nombre']}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        c = canvas.Canvas(nombre_archivo, pagesize=letter)
        width, height = letter

        ruta_imagen = "../web/images/logo.png"  # Cambia esto a la ruta de tu logo

        # Agregar el logo en la parte superior
        c.drawImage(ruta_imagen, x=50, y=height - 70, width=150, height=75, preserveAspectRatio=True, mask='auto')



        # Título
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2.0, height - 40, "Factura de pago - Spa")

        # Información del cliente
        c.setFont("Helvetica", 12)
        y = height - 80
        c.drawString(50, y, f"Cliente: {cliente['nombre']}")
        y -= 20
        c.drawString(50, y, f"Email: {cliente['email']}")
        y -= 20
        c.drawString(50, y, f"Teléfono: {cliente['telefono']}")
        
        # Detalles del servicio y pago
        y -= 40
        c.drawString(50, y, f"Servicio: {servicio['nombre']}")
        y -= 20
        c.drawString(50, y, f"Descripción: {servicio['descripcion']}")
        y -= 20
        c.drawString(50, y, f"Fecha de reserva: {reserva['fecha']}")
        y -= 20
        c.drawString(50, y, f"Monto: ${pago['monto']}")
        y -= 20
        c.drawString(50, y, f"Método de pago: {pago['metodo_pago']}")
        y -= 20
        c.drawString(50, y, f"Fecha de pago: {pago['fecha']}")

        # Guardar el archivo PDF
        c.save()
        return nombre_archivo

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar el PDF: {str(e)}")
@router.post("/enviar_factura")
def enviar_factura_endpoint(reserva_id: int, email_credentials: dict = Body(...)):
    try:
        # Obtener datos de la factura
        datos_factura = crud.obtener_datos_factura(reserva_id)
        if not datos_factura:
            raise HTTPException(status_code=404, detail="Datos de factura no encontrados")

        # Generar la factura en PDF
        archivo_factura = generar_factura_pdf(
            datos_factura['cliente'],
            datos_factura['pago'],
            datos_factura['reserva'],
            datos_factura['servicio']
        )

        # Enviar la factura por email
        enviar_factura_por_email(
            datos_factura['cliente']['email'],
            archivo_factura,
            email_credentials['from_email'],
            email_credentials['from_password']
        )

        return {"mensaje": "Factura enviada con éxito"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.post("/crearPago", response_model=dict)
def create_Pago(pago: Pago):
    return crud.create_pago(pago)


@router.get("/Pagos/")
def get_pagos():
    return crud.get_Payments_xday()
