import os
import subprocess
import time
import logging
import webbrowser
import multiprocessing

def main():
    logging.basicConfig(level=logging.DEBUG, filename="debug.log", filemode="w", format="%(asctime)s - %(levelname)s - %(message)s")

    # Ruta base del proyecto
    base_path = os.path.dirname(os.path.abspath(__file__))
    print(base_path)
    # Ruta del intérprete de Python del sistema en lugar de `sys.executable`
    python_path = os.path.join(base_path, "../env/Scripts", "python.exe")  # O usa la ruta absoluta del intérprete de Python del sistema si es necesario
    print("Python Path:", python_path)

    try:
        # Ejecutar la API en una nueva consola para evitar bloqueos en el ejecutable
        api_process = subprocess.Popen(
            [python_path, "-m", "uvicorn", "main:app"],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )

        # Esperar a que la API se inicie
        time.sleep(2)

        # Ruta de la aplicación Tkinter
        tkinter_app_path = os.path.join(base_path, "../front", "login.py")
        tkinter_process = subprocess.Popen([python_path, tkinter_app_path])

        # Abrir página web principal en el navegador sin bloquear
        webbrowser.open("http://localhost:8000/static/index3.html")

        # Esperar a que la aplicación Tkinter termine
        tkinter_process.wait()

    except KeyboardInterrupt:
        print("Interrupción recibida. Terminando procesos.")
        api_process.terminate()
        tkinter_process.terminate()
    finally:
        # Terminar los procesos si siguen activos
        if api_process.poll() is None:
            api_process.terminate()
        if tkinter_process.poll() is None:
            tkinter_process.terminate()

        # Esperar a que los procesos terminen completamente
        api_process.wait()
        tkinter_process.wait()

        print("Todos los procesos han sido terminados.")

if __name__ == "__main__":
    main()
    multiprocessing.freeze_support()
