from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
# def generar_pdf():
#     pdf = canvas.Canvas("ejemplo.pdf", pagesize=letter)
#     pdf.drawString(100, 750, "Hola, este es un PDF generado en Python.")
#     pdf.save()
# generar_pdf()
#Función para generar PDF de informe de ingresos
def generar_el_pdf_informe_ingresos(datos):
    nombre_archivo = f"informe_ingresos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    width, height = letter
    
    ruta_imagen = "../web/images/logo.png"  # Cambia esto a la ruta de tu logo

    # Agregar el logo en la parte superior
    c.drawImage(ruta_imagen, x=50, y=height - 70, width=150, height=75, preserveAspectRatio=True, mask='auto')
    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2.0, height - 40, "Informe de Ingresos por Tipo de Pago")
    
    # Encabezados de tabla
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 80, "Método de Pago")
    c.drawString(200, height - 80, "Total Ingresos")
    
    # Contenido de la tabla
    c.setFont("Helvetica", 12)
    y = height - 100
    for row in datos:
        metodo_pago = row[0]
        total_ingresos = row[1]
        c.drawString(50, y, metodo_pago)
        c.drawString(200, y, f"{total_ingresos}")
        y -= 20
    
    # Guardar el PDF
    c.save()
    return nombre_archivo


# Función para generar PDF de informe de servicios por profesional
def generar_pdf_informe_servicios(datos):
    nombre_archivo = f"informe_servicios_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    width, height = letter
    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2.0, height - 40, "Informe de Servicios por Profesional")

    # Encabezados de tabla
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 80, "Profesional")
    c.drawString(200, height - 80, "Servicio")
    c.drawString(350, height - 80, "Fecha")

    # Contenido de la tabla
    c.setFont("Helvetica", 12)
    y = height - 100
    for row in datos:
        profesional = row[0]
        servicio = row[1]
        fecha = row[2].strftime('%Y-%m-%d')
        c.drawString(50, y, profesional)
        c.drawString(200, y, servicio)
        c.drawString(350, y, fecha)
        y -= 20

    # Guardar el PDF
    c.save()
    return nombre_archivo
