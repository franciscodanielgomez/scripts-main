import os

# Directorio que contiene las fotos
directory = "fotos webp"

# Obtener la lista de archivos en el directorio
files = os.listdir(directory)

# Sufijo que deseas agregar a los nombres de archivo
suffix = "_2023_10"

for file in files:
    if os.path.isfile(os.path.join(directory, file)):
        # Separar el nombre del archivo y su extensión
        name, extension = os.path.splitext(file)
        
        # Renombrar el archivo con el sufijo
        new_name = name + suffix + extension
        
        # Ruta del archivo original y del nuevo nombre
        old_path = os.path.join(directory, file)
        new_path = os.path.join(directory, new_name)
        
        # Renombrar el archivo
        os.rename(old_path, new_path)

print("Renombrado completado.")

