import json
import pandas as pd

# Nombre del archivo JSON de entrada y CSV de salida
json_file = 'input.json'
csv_file = 'output.csv'

# Leer el archivo JSON
with open(json_file, 'r') as json_data:
    data = json.load(json_data)

# Accede solo a la parte "data" del JSON
data_part = data.get('data', {})

# Convierte la parte "data" en un DataFrame de Pandas
df = pd.DataFrame(data_part).T  # Transponer para tener las claves como columnas

# Guardar el DataFrame en un archivo CSV
df.to_csv(csv_file, index=False)

print(f'Se ha convertido la parte "data" de "{json_file}" a "{csv_file}" con éxito.')

