from typing import List, Dict, Tuple

import itertools
from accounting_templates import plantillas_contables_1
from utils import cargar_plantillas_cuentas
import classes as cl


# Ruta de la plantilla contable
ruta = r"C:\Users\andre\OneDrive\Documentos\Repositories\MIT_Tax_Avoidance\FTZ_Model\directorio_cuentas.xlsx"

# Cargar la plantilla contable
plantilla_1 = cargar_plantillas_cuentas(ruta)


### Diccionario precios:
dict_precios_2 = {
    # Combinaciones de "MKT" como vendedor
    ("MKT", "ZF", "materia_prima"): 5,
    ("MKT", "NCT", "materia_prima"): 5,
    # Combinaciones de "MKT" como comprador
    ("NCT", "MKT", "bien_final"): 7,
    ("ZF", "MKT", "bien_final"): 7,
    # Combinaciones de "NCT" como vendedor
    ("NCT", "ZF", "materia_prima"): 3,
    ("NCT", "ZF", "bien_intermedio"): 5,
    ("NCT", "ZF", "bien_final"): 6,
    # Combinaciones de "ZF" como vendedor
    ("ZF", "NCT", "materia_prima"): 2,
    ("ZF", "NCT", "bien_intermedio"): 4,
    ("ZF", "NCT", "bien_final"): 6,
}

### Instanciar Agentes de NCT y ZF
planta_NCT = cl.NCT("NCT", plantilla_1, plantillas_contables_1)
planta_ZF = cl.ZF("ZF", plantilla_1, plantillas_contables_1)


def calcular_mejor_plan(
    lista_planes: List[List[int]],
    planta_NCT: cl.NCT,
    planta_ZF: cl.ZF,
    dict_precios: Dict[Tuple[str, str, str], float],
) -> Tuple[List[int], float]:
    """
    Calcula el mejor plan basado en la utilidad agregada.

    Args:
        lista_planes: Lista de planes posibles, donde cada plan es una lista de enteros.
        planta_NCT: Instancia de la clase NCT.
        planta_ZF: Instancia de la clase ZF.
        dict_precios: Diccionario de precios para las transacciones.

    Returns:
        Un tuple con el mejor plan y la utilidad agregada asociada.
    """
    mejor_plan = None
    mayor_utilidad = float("-inf")

    for plan in lista_planes:
        # Reiniciar estados contables de las plantas antes de ejecutar el plan
        planta_NCT.reiniciar_estado_contable()
        planta_ZF.reiniciar_estado_contable()

        # Ejecutar el plan
        ejecutor = cl.EjecutorPlan(plan, planta_NCT, planta_ZF, dict_precios)
        ejecutor.ejecutar()

        # Calcular la utilidad agregada
        utilidad_aggregada = (
            planta_NCT.calcular_utilidad_operacional()
            + planta_ZF.calcular_utilidad_operacional()
        )

        # Verificar si es la mayor utilidad encontrada
        if utilidad_aggregada > mayor_utilidad:
            mayor_utilidad = utilidad_aggregada
            mejor_plan = plan

    return mejor_plan, mayor_utilidad


lista_planes = list(itertools.product([0, 1], repeat=3))

calcular_mejor_plan(lista_planes, planta_NCT, planta_ZF, dict_precios_2)
