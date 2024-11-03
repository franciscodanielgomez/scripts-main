import pandas as pd

# Leer el archivo CSV "analizar.csv"
df = pd.read_csv("analizar.csv")

# Crear una lista para almacenar los valores de "Superior" consistentes
valores_consistentes = []

# Iterar a través de los valores únicos en "Superior"
for superior_valor in df["Superior"].unique():
    # Filtrar el DataFrame para un valor específico de "Superior"
    df_filtrado = df[df["Superior"] == superior_valor]
    
    # Verificar si hay al menos un valor diferente en "Precio normal"
    if df_filtrado["Precio normal"].nunique() > 1:
        # Si hay diferencias, agregar el valor de "Superior" a la lista
        valores_consistentes.append(superior_valor)

# Convertir la lista en un DataFrame
df_consistentes = pd.DataFrame({"Superior": valores_consistentes})

# Guardar los valores consistentes en un nuevo archivo CSV llamado "lista.csv"
df_consistentes.to_csv("lista.csv", index=False)

# Imprimir un mensaje indicando el número de valores consistentes en "lista.csv"
print(f"Se han guardado {len(df_consistentes)} valores consistentes en lista.csv")
