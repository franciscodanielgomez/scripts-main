import os

# Directorio que contiene los archivos
directory = "fotos webp"

# Obtener la lista de archivos en el directorio
files = os.listdir(directory)

for file in files:
    if os.path.isfile(os.path.join(directory, file)):
        # Convertir el nombre del archivo a mayúsculas
        name, extension = os.path.splitext(file)
        name_upper = name.upper()
        
        # Renombrar el archivo en mayúsculas
        new_name = name_upper + extension
        
        # Ruta del archivo original y del nuevo nombre
        old_path = os.path.join(directory, file)
        new_path = os.path.join(directory, new_name)
        
        # Renombrar el archivo
        os.rename(old_path, new_path)

print("Renombrado completado.")
