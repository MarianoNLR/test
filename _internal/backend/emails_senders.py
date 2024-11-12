import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from fastapi import HTTPException
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import uvicorn

# Función para generar factura en PDF usando ReportLab

def enviar_factura_por_email(cliente_email, archivo_factura, from_email, from_password):
    to_email = cliente_email

    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = 'Factura de Pago - Spa'

    # Cuerpo del mensaje
    body = "Adjuntamos la factura de tu reserva en el spa. ¡Gracias por tu visita!"
    msg.attach(MIMEText(body, 'plain'))

    # Adjuntar el archivo PDF
    with open(archivo_factura, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename={archivo_factura}")
        msg.attach(part)

    # Enviar el correo
    try:
        # Configuración para Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)  # Usa la contraseña de aplicación aquí
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Correo enviado con éxito a través de Gmail")

    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        raise HTTPException(status_code=500, detail=f"Error en el envío de correo: {e}")