import pandas as pd
import numpy as np
import json
import re
import unicodedata

# Función para extraer los IDs de pagos y productos desde JSON en la columna
def extract_ids(column_data):
    if isinstance(column_data, str):
        try:
            parsed_data = json.loads(column_data.replace("'", "\""))
            return [ref['__ref__'].split('/')[-1] for ref in parsed_data]
        except json.JSONDecodeError:
            return []
    return []

# Función para convertir el formato de la categoría
def format_category(category):
    category = unicodedata.normalize('NFD', category).encode('ascii', 'ignore').decode('utf-8')
    category = re.sub(r'[^a-zA-Z0-9\s]', '', category)
    category = re.sub(r'\s+', ' ', category)
    parts = category.split(' ')
    return ''.join(part.capitalize() if i > 0 else part.lower() for i, part in enumerate(parts))

# Lista de categorías de gráfica
categorias_grafica = [
    'impresionColor', 'ploteoDeCorte', 'talonariosAfip', 'tintasParaAlmohadillas',
    'fotografico180', 'sellosAutomaticos', 'impresionNegro', 'carpetasInstitucionales',
    'lonaLatex', 'letrasCorporeas', 'bond120Gr', 'lapicerasSellos', 'vegetal90Gr',
    'folletos', 'diseno', 'anillados', 'impresionRigidosUv', 'volantes', 'pinesMetalicos',
    'filmPoliester135Gr', 'ijRec135Gr', 'fechadoresYNumeradores', 'ploteoVehicular',
    'sublimacion', 'saldo', 'tarjetasLaser', 'stickers', 'productosTerminadosLatex',
    'viniloUv', 'promo', 'viniloTesis', 'encuadernadoBinder', 'hojasSueltas',
    'soloMaterial', 'encuadernadoTesis', 'impresionRigidosLatex', 'tarjetasOffset',
    'materialesRigidosSolos', 'fotocopias', 'servicios', 'sellosPocketDeBolsillo',
    'sellosDeMadera', 'almohadillas', 'precorte', 'instalacion', 'polipropileno160Gr',
    'sobres', 'viniloLatex', 'textil', 'cambioDeGomaOPolimero', 'recetarios',
    'tarjetasLaserPersonalesCirculares', 'sellosDeMaderaRedondosUOvalados', 'serviciosVinilos',
    'bond90Gr', 'productosTerminadosUv', 'lonaUv', 'hojasMembretadas', 'none',
    'servicioDeCorte', 'almanaques', 'plastificados', 'repuestosParaSellos',
    'serviciosLonas', 'imanes', 'cuadrosDeco', 'cadeteria',
    'fabricacionDeCarteles', 'fotogr180Gr'
]

def procesar_datos(df, date_column):
    resultados = pd.DataFrame()
    resultados['date'] = sorted(df[date_column].unique())
    
    for categoria in categorias_grafica:
        suma_categoria = df[df['category'] == categoria].groupby(date_column)['weighted_average'].sum()
        resultados[categoria] = resultados['date'].map(suma_categoria).fillna(0)
    
    resultados['subtotalgrafica'] = resultados[categorias_grafica].sum(axis=1)
    subtotal_libreria = df[~df['category'].isin(categorias_grafica)].groupby(date_column)['weighted_average'].sum()
    resultados['subtotallibreria'] = resultados['date'].map(subtotal_libreria).fillna(0)
    resultados['total'] = resultados['subtotalgrafica'] + resultados['subtotallibreria']
    
    columnas_ordenadas = ['date'] + categorias_grafica + ['subtotalgrafica', 'subtotallibreria', 'total']
    return resultados[columnas_ordenadas]

def main():
    # Cargar los archivos CSV iniciales
    mostrador_df = pd.read_csv('mostrador.csv')
    pagos_df = pd.read_csv('pagos.csv')
    products_df = pd.read_csv('products.csv')
    caja_df = pd.read_csv('caja.csv')

    # Procesar mostrador_df
    mostrador_df['pagos'] = mostrador_df['pagos'].apply(extract_ids)
    mostrador_df['products'] = mostrador_df['products'].apply(extract_ids)

    # Crear diccionarios para acceso rápido
    pagos_dict = pagos_df.set_index('id_pagos').to_dict(orient='index')
    products_dict = products_df.set_index('id_products')
    categories_dict = products_dict['category'].to_dict()

    # Procesar datos principales
    final_data = []
    for _, row in mostrador_df.iterrows():
        total = row['total']
        product_ids = row['products']
        
        subtotal_list = [float(products_dict.loc[prod_id, 'subtotal']) for prod_id in product_ids if prod_id in products_dict.index]
        categories_list = [categories_dict[prod_id] for prod_id in product_ids if prod_id in categories_dict]
        
        for pago_id in row['pagos']:
            if pago_id in pagos_dict:
                amount = pagos_dict[pago_id]['amount']
                created = pagos_dict[pago_id]['created']
                
                weighted_average_list = [(subtotal / total) * amount if total != 0 else 0 for subtotal in subtotal_list]
                
                final_data.append({
                    'total': total,
                    'id_pagos': pago_id,
                    'amount': amount,
                    'created': created,
                    'subtotal_list': tuple(subtotal_list),
                    'product_ids': tuple(product_ids),
                    'categories': tuple(categories_list),
                    'weighted_average': tuple(weighted_average_list)
                })

    # Crear y procesar new_df
    new_data = []
    for row in final_data:
        created = row['created']
        categories = row['categories']
        weighted_averages = row['weighted_average']
        
        if len(categories) == len(weighted_averages):
            for category, weighted_average in zip(categories, weighted_averages):
                if isinstance(category, str):
                    new_data.append({
                        'created': created,
                        'category': format_category(category.strip().strip("'")),
                        'weighted_average': float(weighted_average)
                    })

    new_df = pd.DataFrame(new_data)
    new_df['date'] = pd.to_datetime(new_df['created'])
    new_df['date_day'] = new_df['date'].dt.date
    new_df['date_month'] = new_df['date'].dt.to_period('M')

    # Generar resultados diarios
    resultados_diarios = procesar_datos(new_df, 'date_day')
    
    # Procesar datos de caja
    caja_df['fecha'] = pd.to_datetime(caja_df['creado']).dt.date
    
    # Fusionar resultados diarios con datos de caja
    resultado_fusionado = resultados_diarios.merge(
        caja_df[['fecha', 'impresionBN', 'impresionC', 'impresionFotocopia']], 
        left_on='date', right_on='fecha', 
        how='left'
    )
    
    # Limpiar y procesar resultado_fusionado
    resultado_fusionado.fillna(0, inplace=True)
    resultado_fusionado.drop(columns=['fecha'], inplace=True)
    
    # Calcular diferencias y relaciones
    impresion_cols = {
        'C': ('impresionC', 'impresionColor'),
        'BN': ('impresionBN', 'impresionNegro'),
        'Fotocopia': ('impresionFotocopia', 'fotocopias')
    }

    for suffix, (col, target) in impresion_cols.items():
        # Calcular diferencia
        diff_col = f'diferencia_{col}'
        resultado_fusionado[diff_col] = resultado_fusionado[col] - resultado_fusionado[col].shift(1)
        resultado_fusionado.loc[resultado_fusionado[col].shift(1) == 0, diff_col] = None
        resultado_fusionado[diff_col] = resultado_fusionado[diff_col].clip(lower=0)
        resultado_fusionado.loc[resultado_fusionado[diff_col].abs() >= 10000, diff_col] = 0
        
        # Calcular relación
        resultado_fusionado[f'relation{suffix}'] = np.where(
            resultado_fusionado[diff_col] != 0,
            resultado_fusionado[target] / resultado_fusionado[diff_col],
            0
        )
    
    # Guardar resultado_fusionado.csv
    resultado_fusionado.to_csv('resultado_fusionado.csv', index=False)
    
    # Procesar datos mensuales
    resultado_fusionado['month_year'] = pd.to_datetime(resultado_fusionado['date']).dt.to_period('M')
    
    # Identificar columnas a sumar
    cols_to_sum = categorias_grafica + [
        'subtotalgrafica', 'subtotallibreria', 'total',
        'diferencia_impresionC', 'diferencia_impresionBN', 'diferencia_impresionFotocopia'
    ]
    
    # Generar resultado mensual
    resultado_mensual = resultado_fusionado.groupby('month_year')[cols_to_sum].sum()
    
    # Calcular promedios mensuales para las relaciones
    for suffix, (col, _) in impresion_cols.items():
        resultado_mensual[f'relation{suffix}'] = resultado_fusionado.groupby('month_year')[f'relation{suffix}'].mean()
    
    # Formatear y guardar resultado mensual
    resultado_mensual.reset_index(inplace=True)
    resultado_mensual['month_year'] = resultado_mensual['month_year'].dt.strftime('%Y-%m')
    resultado_mensual.to_csv('resultado_mensual.csv', index=False)

if __name__ == "__main__":
    main()
