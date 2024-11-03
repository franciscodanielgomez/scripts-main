import pandas as pd
import numpy as np

# Cargar los archivos CSV en DataFrames
lista_correcta = pd.read_csv('Lista Correcta.csv')
lista_analizar = pd.read_csv('Lista Analizar.csv')

# Reemplazar los valores no válidos ('#VALUE!') con NaN en ambas columnas 'normal'
lista_correcta['normal'] = lista_correcta['normal'].replace('#VALUE!', np.nan)
lista_analizar['normal'] = lista_analizar['normal'].replace('#VALUE!', np.nan)

# Convertir las columnas 'normal' a números enteros (si es posible)
lista_correcta['normal'] = lista_correcta['normal'].astype(float)
lista_analizar['normal'] = lista_analizar['normal'].astype(float)

# Combinar DataFrames por SKU y realizar la comparación
resultado = lista_analizar.merge(lista_correcta, on='sku', suffixes=('_analizar', '_correcta'))

# Crear una columna 'Precio Rebajado Correcto' si el Precio Normal Analizar es menor
def calcular_precio_rebajado_correcto(row):
    precio_normal_analizar = row['normal_analizar']
    precio_normal_correcta = row['normal_correcta']
    
    if pd.notna(precio_normal_analizar) and pd.notna(precio_normal_correcta):
        return min(precio_normal_analizar, precio_normal_correcta)
    elif pd.notna(precio_normal_analizar):
        return precio_normal_analizar
    elif pd.notna(precio_normal_correcta):
        return precio_normal_correcta
    else:
        return None

resultado['Precio Rebajado Correcto'] = resultado.apply(calcular_precio_rebajado_correcto, axis=1)

# Agregar el precio normal correcto y el precio rebajado correcto al resultado
resultado['Precio Normal Correcto'] = resultado['normal_correcta']
resultado['Precio Rebajado Correcto'] = resultado['rebajado_correcta']

# Seleccionar las columnas requeridas en el resultado
resultado = resultado[['sku', 'rebajado_analizar', 'Precio Normal Correcto', 'Precio Rebajado Correcto']]

# Guardar el resultado en un nuevo archivo CSV
resultado.to_csv('Resultado.csv', index=False)
