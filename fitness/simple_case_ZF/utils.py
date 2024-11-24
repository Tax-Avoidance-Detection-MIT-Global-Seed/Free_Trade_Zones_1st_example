import pandas as pd
from pathlib import Path

PATH = str((Path(__file__).resolve()).parent)
excel_file_name = r"/directorio_cuentas.xlsx"

def cargar_plantillas_cuentas(archivo_excel: str) -> dict:
    """
    Función para cargar los tipos de cuenta que funcionaran en el modelo

    """
    # Cargar el archivo Excel en un DataFrame
    df = pd.read_excel(archivo_excel, sheet_name="cuentas_modelo")

    # Inicializar el diccionario para almacenar las plantillas
    plantillas_cuentas = {}

    # Iterar sobre las filas del DataFrame
    for _, row in df.iterrows():    
        codigo_cuenta = row["codigo_cuenta"]
        codigo_tipo = row["tipo_de_cuenta "]
        cuenta = row["cuenta"]

        # Guardar los datos en el diccionario
        plantillas_cuentas[codigo_cuenta] = {
            "codigo_tipo_cuenta": codigo_tipo,
            "cuenta": cuenta,
        }

    # Devolver el diccionario con la estructura cargada
    return plantillas_cuentas


df_test = cargar_plantillas_cuentas(PATH + excel_file_name)
