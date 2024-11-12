import os
from PIL import Image, ImageTk
import subprocess

"""​​Che siguiendo con mi pregunta de Chaqueño, 
obviamente voy a intentar 
improve my inglsh, pero para subir a SemiSR, que considerarias 
que debe saber alguien? para hacerlo con freelance o proyectos propios"""
"""Che continuando con mi pregunta de Junior Chaqueño, 
que consideras que deberia de aprender en base a 
proyectos propios para considerarme SemiSenior? I
ntentare Improve mi englis"""
# Función para cargar imágenes de manera segura
def load_image(image_filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_dir, 'images', image_filename)
    try:
        image = Image.open(image_path)
        return image
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar la imagen '{image_path}'")
        return None

# Función para ejecutar otros scripts de frontend (por ejemplo, register.py, etc.)
def open_script(script_name):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(base_dir, script_name)

    # Obtener la ruta del intérprete de Python en el entorno virtual
    python_path = os.path.join(base_dir, '..', 'env', 'Scripts', 'python.exe')

    # Ejecutar el archivo de Python usando el intérprete del entorno virtual
    print(python_path)
    subprocess.Popen([python_path, script_path])
