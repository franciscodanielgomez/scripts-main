import pandas as pd

# Leer el archivo CSV
try:
    df = pd.read_csv('pedidos.csv')
except FileNotFoundError:
    print("Error: El archivo 'pedidos.csv' no se encontró. Verifica la ruta.")
    exit()

# Verificar que el archivo contiene la columna 'cliente.__ref__'
if 'cliente.__ref__' not in df.columns:
    print("Error: El archivo CSV no contiene la columna 'cliente.__ref__'.")
    exit()

# Verificar si la columna 'tipo' existe y filtrar solo si está presente
if 'tipo' in df.columns:
    # Filtrar los pedidos que no sean de tipo "Presupuesto"
    df_filtered = df[df['tipo'] != 'Presupuesto']
else:
    # Si no hay columna 'tipo', no aplicar ningún filtro
    df_filtered = df

# Verificar si hay datos después de filtrar
if df_filtered.empty:
    print("Error: No hay datos después de filtrar los pedidos.")
    exit()

# Asegurarse de que las columnas 'total' y 'parcial' son numéricas
df_filtered['total'] = pd.to_numeric(df_filtered['total'], errors='coerce')
df_filtered['parcial'] = pd.to_numeric(df_filtered['parcial'], errors='coerce')

# Agrupar por el campo cliente.__ref__ (que será el 'user')
grouped = df_filtered.groupby('cliente.__ref__').agg(
    total=('total', 'sum'),
    parcial=('parcial', 'sum')
).reset_index()

# Calcular el saldo (total - parcial)
grouped['saldo'] = grouped['total'] - grouped['parcial']

# Crear la columna 'id' extrayendo el valor después de 'users-iconos/'
grouped['id'] = grouped['cliente.__ref__'].str.split('/').str[-1]

# Renombrar 'cliente.__ref__' a 'user'
grouped.rename(columns={'cliente.__ref__': 'user'}, inplace=True)

# Redondear las columnas total, parcial y saldo a 2 decimales
grouped['total'] = grouped['total'].round(2)
grouped['parcial'] = grouped['parcial'].round(2)
grouped['saldo'] = grouped['saldo'].round(2)

# Reordenar las columnas para que 'id' aparezca primero
grouped = grouped[['id', 'user', 'total', 'parcial', 'saldo']]

# Guardar el resultado en un nuevo CSV
grouped.to_csv('saldo_clientes.csv', index=False)

print("Lista de saldo de clientes con valores redondeados a 2 decimales generada con éxito.")
