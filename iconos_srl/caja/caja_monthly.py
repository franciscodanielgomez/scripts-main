import pandas as pd

# Cargar el archivo CSV
file_path = 'caja.csv'
df = pd.read_csv(file_path)

# Convertir la columna 'creado' a formato datetime
df['creado'] = pd.to_datetime(df['creado'], format='%Y-%m-%d %H:%M:%S')

# Reemplazar NaN por 0 para las columnas de venta antes de sumar
df.fillna(0, inplace=True)

# Crear las nuevas columnas de ventas
df['ventaLibreriaTotal'] = df['ventaLefectivo'] + df['ventaLcheque'] + df['ventaLposnet'] + df['ventaLtransferencia'] + df['ventaLmp']
df['ventaGraficaTotal'] = (df['ventaMefectivo'] + df['ventaMdebito'] + df['ventaMcheque'] + df['ventaMposnet'] + 
                           df['ventaMtransferencia'] + df['ventaMmp'] + df['ventaPefectivo'] + df['ventaPdebito'] + 
                           df['ventaPcheque'] + df['ventaPposnet'] + df['ventaPtransferencia'] + df['ventaPmp'])
df['ventaTotal'] = df['ventaLibreriaTotal'] + df['ventaGraficaTotal']

# Seleccionar solo las columnas numéricas
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns

# Agrupar por año y mes, sumando solo las columnas numéricas
monthly_sums = df.groupby(df['creado'].dt.to_period('M'))[numeric_cols].sum()

# Redondear los valores a dos decimales
monthly_sums = monthly_sums.round(2)

# Guardar el resultado en un nuevo archivo CSV en el mismo directorio
output_file = 'caja_mensual.csv'
monthly_sums.to_csv(output_file)

print(f"Archivo generado: {output_file}")
