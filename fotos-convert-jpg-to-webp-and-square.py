from PIL import Image
import os

# Directorio que contiene las imágenes en formato .jpg
input_directory = "fotos jpg"

# Directorio donde se guardarán las imágenes convertidas en formato .webp
output_directory = "fotos webp"

# Asegurarse de que el directorio de salida exista, si no, crearlo
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Obtener la lista de archivos en el directorio de entrada
image_files = os.listdir(input_directory)

for image_file in image_files:
    if image_file.endswith(".jpg"):
        # Cargar la imagen .jpg
        image = Image.open(os.path.join(input_directory, image_file))
        
        # Obtener las dimensiones de la imagen
        width, height = image.size
        
        # Calcular el tamaño máximo para hacer la imagen cuadrada
        max_size = max(width, height)
        
        # Crear una nueva imagen cuadrada con fondo blanco
        new_image = Image.new("RGB", (max_size, max_size), (255, 255, 255))
        
        # Pegar la imagen original en el centro de la nueva imagen
        x_offset = (max_size - width) // 2
        y_offset = (max_size - height) // 2
        new_image.paste(image, (x_offset, y_offset))
        
        # Construir la ruta de salida con el mismo nombre de archivo pero con extensión .webp
        output_file = os.path.join(output_directory, os.path.splitext(image_file)[0] + ".webp")
        
        # Convertir y guardar la imagen en formato .webp
        new_image.save(output_file, "webp")

print("Conversión completada.")

