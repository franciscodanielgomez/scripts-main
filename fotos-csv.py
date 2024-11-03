import glob
import csv
import os

URL_PREFIX = "https://royalmayorista.com.ar/wp-content/uploads/2023/10/"

files = glob.glob("./*.webp")

with open("Nuevas.csv", "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    
    # Agregar encabezados de las columnas
    csv_writer.writerow(["SKU", "Imágenes", "Publicado"])
    
    for file in files:
        # Obtener el nombre del archivo sin la extensión ".webp"
        file_name = os.path.splitext(os.path.basename(file))[0]
        
        # Verificar si el nombre de archivo contiene "-" o espacios
        if "-" not in file_name and " " not in file_name:
            url = URL_PREFIX + file_name + "-scaled.webp"  # Agregar "-scaled.webp" al final
            
            # Agregar una fila al archivo CSV con el valor "1" en la columna "Publicado"
            csv_writer.writerow([file_name, url, 1])

print("Exportación a CSV completada.")
