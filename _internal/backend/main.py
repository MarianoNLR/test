import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from routers import clients, payments, reports, reservations, services, workers 


app = FastAPI()


       # Configuración de CORS
origins = [
    "http://localhost/",
    "http://localhost:8000/",
    "http://127.0.0.1/",
    "http://127.0.0.1:8000/",
]

app.addmiddleware(
    CORSMiddleware,
    alloworigins=[""],  # Allow all origins temporarily
    allow_credentials=True,
    allow_methods=[""],
    allowheaders=["*"],
)


app.includerouter(clients.router)
app.includerouter(services.router)
app.includerouter(reservations.router)
app.include_router(payments.router)
app.include_router(reports.router) 
app.include_router(workers.router)

    # Sirviendo archivos estáticos desde "web"
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file), "../web")), name="static")

Directorio de plantillas (HTML dinámico)
templates = Jinja2Templates(directory="web")

@app.get("/")
async def read_index(request: Request):
    # Puedes pasar datos dinámicos al template
    return templates.TemplateResponse("index3.html", {"request": request, "message": "Bienvenido a Spa Sentirse Bien"})
def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name == "__main":
    main()