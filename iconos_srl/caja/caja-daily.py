import pandas as pd

# Cargar el CSV
df = pd.read_csv('caja.csv')

# Convertir la columna 'creado' a formato datetime para asegurar que los datos están en el formato correcto
df['creado'] = pd.to_datetime(df['creado'], errors='coerce')

# Completar 'dia', 'mes', y 'year' basándonos en la columna 'creado'
df['dia'] = df['creado'].dt.day.fillna(df['dia'])
df['mes'] = df['creado'].dt.month.fillna(df['mes'])
df['year'] = df['creado'].dt.year.fillna(df['year'])

# Convertir 'dia', 'mes', y 'year' a enteros (en caso de que se hayan completado como flotantes)
df['dia'] = df['dia'].astype(int)
df['mes'] = df['mes'].astype(int)
df['year'] = df['year'].astype(int)

# Especificar las columnas que no deben ser sumadas, sino que deben tomar el primer o último valor
columns_first = ['ID', 'id', 'dia', 'mes', 'year', 'responsableCreador', 'responsableCierre', 'cerrado', 'creado', 'montoInicial']
columns_last = ['montoFinal']

# Especificar las columnas que deben ser sumadas
columns_to_sum = [col for col in df.columns if col not in columns_first + columns_last]

# Agrupar por día, mes y año, obteniendo el primer valor para 'montoInicial', el último valor para 'montoFinal' y sumando las demás columnas
df_grouped = df.groupby(['dia', 'mes', 'year'], as_index=False).agg(
    {**{col: 'first' for col in columns_first}, 
       **{col: 'last' for col in columns_last},
       **{col: 'sum' for col in columns_to_sum}}
)

# Ajustar la columna 'creado' después de la agrupación, tomando el primer valor y formateándolo
df_grouped['creado'] = df_grouped['creado'].dt.strftime('%Y-%m-%d 00:00:00')

# Redondear las columnas numéricas a dos decimales
for col in columns_to_sum:
    if pd.api.types.is_numeric_dtype(df_grouped[col]):
        df_grouped[col] = df_grouped[col].round(2)

# Guardar el resultado en un nuevo archivo CSV
df_grouped.to_csv('cierre.csv', index=False)

print("Archivo de cierre de cajas agrupado por día guardado como 'cierre_cajas_agrupado.csv'.")
