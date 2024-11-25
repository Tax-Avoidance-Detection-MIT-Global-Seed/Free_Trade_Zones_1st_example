from typing import List, Dict, Tuple
from pathlib import Path
import itertools

from accounting_templates import plantillas_contables_1, dict_precios_2
from utils import cargar_plantillas_cuentas
import classes as cl


PATH = str((Path(__file__).resolve()).parent)
excel_file_name = r"/directorio_cuentas.xlsx"

# TODO mejorar el manejo de cl
# TODO Integrar los agentes directamente en la calculadora, para que la calculadora pueda tratar con una lista de agentes

# Cargar la plantilla contable
plantilla_1 = cargar_plantillas_cuentas(PATH + excel_file_name)


### Instanciar Agentes de NCT y ZF
planta_NCT = cl.NCT("NCT", plantilla_1, plantillas_contables_1)
planta_ZF = cl.ZF("ZF", plantilla_1, plantillas_contables_1)


lista_planes = list(itertools.product([0, 1], repeat=3))


mejor_plan = None
mejor_utilidad = float("-inf")  # Inicializar con el menor valor posible

for plan in lista_planes:
    planta_NCT.reiniciar_estado_contable()
    planta_ZF.reiniciar_estado_contable()
    ejecutor = cl.EjecutorPlan(plan, planta_NCT, planta_ZF, dict_precios_2)
    ejecutor.ejecutar()

    u1 = planta_NCT.generar_estado_resultados()
    u2 = planta_ZF.generar_estado_resultados()

    W = (
        planta_NCT.calcular_utilidad_operacional()
        + planta_ZF.calcular_utilidad_operacional()
    )

    # Verificar si este plan tiene la mejor utilidad
    if W > mejor_utilidad:
        mejor_utilidad = W
        mejor_plan = plan

    print("-------------------------------------")
    print(
        f"plan:{plan}",
        planta_NCT.generar_estado_resultados(),
        planta_ZF.generar_estado_resultados(),
        f"Utilidad: {W}",
    )
    print("-------------------------------------")

# Mostrar el mejor plan al final
print("\n=====================================")
print("El mejor plan es:")
print(f"Plan: {mejor_plan}")
print(f"Utilidad: {mejor_utilidad}")
print("=====================================")
