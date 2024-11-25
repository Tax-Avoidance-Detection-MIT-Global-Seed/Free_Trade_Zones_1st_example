from typing import List, Dict, Tuple
from pathlib import Path
import itertools

# Graficar distancia vs utilidad
import matplotlib.pyplot as plt
from accounting_templates import plantillas_contables_1, dict_precios_2
from utils import cargar_plantillas_cuentas
import classes as cl
import pandas as pd


PATH = str((Path(__file__).resolve()).parent)
excel_file_name = r"/directorio_cuentas.xlsx"

# TODO mejorar el manejo de cl
# TODO Integrar los agentes directamente en la calculadora, para que la calculadora pueda tratar con una lista de agentes

# Cargar la plantilla contable
plantilla_1 = cargar_plantillas_cuentas(PATH + excel_file_name)


# Definir los diccionarios


##### ---------------------------------------- Funcion de generacion de diccionarios -----------


def generar_diccionarios_materia_prima(dict_precios_base, rango_distancia=(-10, 10)):
    """
    Genera un rango de diccionarios basados en las condiciones dadas:
    1) Precios no negativos.
    2) La diferencia entre los dos primeros precios varía en un rango dado.

    Args:
    - dict_precios_base (dict): Diccionario base con precios.
    - rango_distancia (tuple): Rango de la distancia entre los dos primeros precios.

    Returns:
    - list: Lista de diccionarios que cumplen con las condiciones.
    """
    dicts_generados = []

    # Obtener las claves de los dos primeros precios
    keys = list(dict_precios_base.keys())
    key1, key2 = keys[0], keys[1]

    # Valores iniciales de los dos primeros precios
    precio1_inicial = dict_precios_base[key1]
    precio2_inicial = dict_precios_base[key2]

    for distancia in range(rango_distancia[0], rango_distancia[1] + 1):
        # Calcular nuevos precios basados en la distancia
        nuevo_precio1 = max(1, precio1_inicial + distancia)
        nuevo_precio2 = max(1, precio2_inicial - distancia)

        # Crear una copia del diccionario base
        nuevo_diccionario = dict_precios_base.copy()

        # Actualizar los precios de las dos primeras claves
        nuevo_diccionario[key1] = nuevo_precio1
        nuevo_diccionario[key2] = nuevo_precio2

        # Añadir el nuevo diccionario a la lista
        dicts_generados.append(nuevo_diccionario)

    return dicts_generados


# Diccionario base
dict_precios_base = {
    # Combinaciones de "MKT" como vendedor
    ("MKT", "ZF", "materia_prima"): 3,
    ("MKT", "NCT", "materia_prima"): 3,
    # Combinaciones de "MKT" como comprador
    ("NCT", "MKT", "bien_final"): 20,
    ("ZF", "MKT", "bien_final"): 20,
    # Combinaciones de "NCT" como vendedor
    ("NCT", "ZF", "materia_prima"): 4,
    ("NCT", "ZF", "bien_intermedio"): 5,
    ("NCT", "ZF", "bien_final"): 6,
    # Combinaciones de "ZF" como vendedor
    ("ZF", "NCT", "materia_prima"): 4,
    ("ZF", "NCT", "bien_intermedio"): 5,
    ("ZF", "NCT", "bien_final"): 6,
}

# Generar el rango de diccionarios
rango_diccionarios = generar_diccionarios_materia_prima(
    dict_precios_base, rango_distancia=(-10, 10)
)

# Imprimir algunos ejemplos
for i, diccionario in enumerate(rango_diccionarios[:5], 1):
    print(f"Diccionario {i}: {diccionario}")


#### ---------------------------- Función de mejor plan dado un diccionario


def mejor_plan(diccionario: Dict[Tuple[str, str, str], float]):
    lista_planes = list(
        itertools.product([0, 1], repeat=3)
    )  # lista de planes a evaluar

    planta_NCT = cl.NCT("NCT", plantilla_1, plantillas_contables_1)
    planta_ZF = cl.ZF("ZF", plantilla_1, plantillas_contables_1)

    mejor_plan = None
    mejor_utilidad = float("-inf")  # Inicializar con el menor valor posible

    for plan in lista_planes:
        planta_NCT.reiniciar_estado_contable()
        planta_ZF.reiniciar_estado_contable()
        ejecutor = cl.EjecutorPlan(plan, planta_NCT, planta_ZF, diccionario)
        ejecutor.ejecutar()

        W = (
            planta_NCT.calcular_utilidad_operacional()
            + planta_ZF.calcular_utilidad_operacional()
        )

        # Verificar si este plan tiene la mejor utilidad
        if W > mejor_utilidad:
            mejor_utilidad = W
            mejor_plan = plan
    return mejor_plan, mejor_utilidad


#### ------------------------------ Función Distancias entre los precios de compra de materia prima


def distancia_vs_mejor_plan(diccionario: Dict[Tuple[str, str, str], float]):
    """
    Calcula la distancia entre los dos primeros precios en el diccionario,
    obtiene el mejor plan y la mejor utilidad, y retorna los resultados.

    Args:
    - diccionario (Dict[Tuple[str, str, str], float]): Diccionario con precios.

    Returns:
    - Tuple[Dict[Tuple[str, str, str], float], Any, float, float]:
        El diccionario actualizado, el mejor plan, la mejor utilidad,
        y la distancia entre los dos primeros precios.
    """
    # Obtener las claves de los dos primeros precios
    keys = list(diccionario.keys())
    key1, key2 = keys[0], keys[1]

    # Valores iniciales de los dos primeros precios
    precio1 = diccionario[key1]
    precio2 = diccionario[key2]

    # Calcular la distancia entre los dos primeros precios
    distancia = precio1 - precio2

    # Calcular el mejor plan y la mejor utilidad
    mejor_plan_resultado, mejor_utilidad = mejor_plan(diccionario)

    return mejor_plan_resultado, mejor_utilidad, distancia


### Loop de grafica


# Inicializa la lista para guardar la información
resultados = []

# Itera sobre los diccionarios en rango_diccionarios
for diccionario in rango_diccionarios:
    # Obtén los resultados para el diccionario actual
    mejor_plan_resultado, mejor_utilidad, distancia = distancia_vs_mejor_plan(
        diccionario
    )

    # Guarda los resultados en un diccionario
    resultado = {
        "distancia": distancia,
        "mejor_plan": mejor_plan_resultado,
        "utilidad": mejor_utilidad,
    }

    # Agrega el diccionario a la lista de resultados
    resultados.append(resultado)


# Convierte la lista de resultados en un DataFrame para facilitar la visualización y graficado
df_resultados = pd.DataFrame(resultados)

# Visualiza los primeros resultados para verificar
print(df_resultados.head())


plt.figure(figsize=(10, 6))
plt.plot(df_resultados["distancia"], df_resultados["utilidad"], label="Utilidad")
plt.title("Distancia vs Utilidad")
plt.xlabel("Distancia")
plt.ylabel("Utilidad")
plt.legend()
plt.grid()
plt.show()

# Graficar distancia vs mejor plan
plt.figure(figsize=(10, 6))
df_resultados["mejor_plan_encoded"] = pd.factorize(df_resultados["mejor_plan"])[0]
plt.scatter(
    df_resultados["distancia"], df_resultados["mejor_plan_encoded"], label="Mejor Plan"
)
plt.title("Distancia vs Mejor Plan")
plt.xlabel("Distancia")
plt.ylabel("Mejor Plan (codificado)")
plt.legend()
plt.grid()
plt.show()


####------------------------- Distancias entre los precios de materia prima y de bien intermedio (simétricos)


def generar_diccionarios_mp_bi(dict_precios_base, rango_distancia=(-10, 10)):
    """
    Genera un rango de diccionarios basados en las condiciones dadas:
    1) Precios no negativos.
    2) La diferencia entre los dos primeros precios varía en un rango dado.

    Args:
    - dict_precios_base (dict): Diccionario base con precios.
    - rango_distancia (tuple): Rango de la distancia entre los dos primeros precios.

    Returns:
    - list: Lista de diccionarios que cumplen con las condiciones.
    """
    dicts_generados = []

    # Obtener las claves de los dos primeros precios
    keys = list(dict_precios_base.keys())
    key1, key5 = keys[0], keys[5]

    # Valores iniciales de los dos primeros precios
    p_x = dict_precios_base[key1]
    p_y = dict_precios_base[key5]

    for distancia in range(rango_distancia[0], rango_distancia[1] + 1):
        # Calcular nuevos precios basados en la distancia
        nuevo_p_x = max(1, p_x + distancia)
        nuevo_p_y = max(1, p_y - distancia)

        # Crear una copia del diccionario base
        nuevo_diccionario = dict_precios_base.copy()

        # Actualizar los precios de las dos primeras claves
        nuevo_diccionario[keys[0]] = nuevo_p_x
        nuevo_diccionario[keys[1]] = nuevo_p_x

        nuevo_diccionario[keys[5]] = nuevo_p_y
        nuevo_diccionario[keys[8]] = nuevo_p_y

        # Añadir el nuevo diccionario a la lista
        dicts_generados.append(nuevo_diccionario)

    return dicts_generados


def distancia_vs_mejor_plan_mp_bi(diccionario: Dict[Tuple[str, str, str], float]):
    """
    Calcula la distancia entre los dos primeros precios en el diccionario,
    obtiene el mejor plan y la mejor utilidad, y retorna los resultados.

    Args:
    - diccionario (Dict[Tuple[str, str, str], float]): Diccionario con precios.

    Returns:
    - Tuple[Dict[Tuple[str, str, str], float], Any, float, float]:
        El diccionario actualizado, el mejor plan, la mejor utilidad,
        y la distancia entre los dos primeros precios.
    """
    # Obtener las claves de los dos primeros precios
    keys = list(diccionario.keys())
    key1, key2 = keys[0], keys[5]

    # Valores iniciales de los dos primeros precios
    precio1 = diccionario[key1]
    precio2 = diccionario[key2]

    # Calcular la distancia entre los dos primeros precios
    distancia = precio1 - precio2

    # Calcular el mejor plan y la mejor utilidad
    mejor_plan_resultado, mejor_utilidad = mejor_plan(diccionario)

    return mejor_plan_resultado, mejor_utilidad, distancia


rango_diccionarios_2 = generar_diccionarios_mp_bi(
    dict_precios_base, rango_distancia=(-10, 10)
)


# Inicializa la lista para guardar la información
resultados_2 = []

# Itera sobre los diccionarios en rango_diccionarios
for diccionario in rango_diccionarios_2:
    # Obtén los resultados para el diccionario actual
    mejor_plan_resultado, mejor_utilidad, distancia = distancia_vs_mejor_plan_mp_bi(
        diccionario
    )

    # Guarda los resultados en un diccionario
    resultado = {
        "distancia": distancia,
        "mejor_plan": mejor_plan_resultado,
        "utilidad": mejor_utilidad,
    }

    # Agrega el diccionario a la lista de resultados
    resultados_2.append(resultado)


# Convierte la lista de resultados en un DataFrame para facilitar la visualización y graficado
df_resultados_2 = pd.DataFrame(resultados_2)

# Visualiza los primeros resultados para verificar
print(df_resultados_2.head())


plt.figure(figsize=(10, 6))
plt.plot(df_resultados_2["distancia"], df_resultados_2["utilidad"], label="Utilidad")
plt.title("Distancia Materia prima - Bien intermedio vs Utilidad")
plt.xlabel("Distancia Materia prima - Bien intermedio")
plt.ylabel("Utilidad")
plt.legend()
plt.grid()
plt.show()

# Graficar distancia vs mejor plan
plt.figure(figsize=(10, 6))
df_resultados_2["mejor_plan_encoded"] = pd.factorize(df_resultados_2["mejor_plan"])[0]
plt.scatter(
    df_resultados_2["distancia"],
    df_resultados_2["mejor_plan_encoded"],
    label="Mejor Plan",
)
plt.title("Distancia vs Mejor Plan")
plt.xlabel("Distancia")
plt.ylabel("Mejor Plan (codificado)")
plt.legend()
plt.grid()
plt.show()
