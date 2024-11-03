import os
import re

# Directorio que contiene los archivos
directory = "fotos webp"

# Obtener la lista de archivos en el directorio
files = os.listdir(directory)

for file in files:
    if os.path.isfile(os.path.join(directory, file)):
        # Obtener el nombre del archivo sin la extensión ".webp"
        file_name, file_extension = os.path.splitext(file)
        
        # Verificar si el nombre del archivo contiene caracteres no alfanuméricos, "(", ")", "-", o espacios
        if re.search(r'[^A-Za-z0-9() -]', file_name) or " " in file_name or "-" in file_name:
            # Construir la ruta del archivo
            file_path = os.path.join(directory, file)
            
            # Eliminar el archivo
            os.remove(file_path)
            print(f"Archivo eliminado: {file_path}")

print("Eliminación de archivos completada.")

