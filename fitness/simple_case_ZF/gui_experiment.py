import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Tuple
import itertools
from pathlib import Path 

import classes as cl
from utils import cargar_plantillas_cuentas
from accounting_templates import plantillas_contables_1

PATH = str((Path(__file__).resolve()).parent)
excel_file_name = r"/directorio_cuentas.xlsx"

# Cargar plantilla contable 
plantilla_1 = cargar_plantillas_cuentas(PATH + excel_file_name)

# TODO Revisar la importación del script classes 

# Agentes
planta_NCT = cl.NCT("NCT", plantilla_1, plantillas_contables_1)
planta_ZF = cl.ZF("ZF", plantilla_1, plantillas_contables_1)

# Diccionario inicial
dict_precios_2 = {
    ("MKT", "ZF", "materia_prima"): 5,
    ("MKT", "NCT", "materia_prima"): 5,
    ("NCT", "MKT", "bien_final"): 7,
    ("ZF", "MKT", "bien_final"): 7,
    ("NCT", "ZF", "materia_prima"): 3,
    ("NCT", "ZF", "bien_intermedio"): 5,
    ("NCT", "ZF", "bien_final"): 6,
    ("ZF", "NCT", "materia_prima"): 2,
    ("ZF", "NCT", "bien_intermedio"): 4,
    ("ZF", "NCT", "bien_final"): 6,
}


# Función a optimizar
def calcular_mejor_plan(
    lista_planes: List[List[int]],
    planta_NCT: cl.NCT,
    planta_ZF: cl.ZF,
    dict_precios: Dict[Tuple[str, str, str], float],
) -> Tuple[List[int], float]:
    mejor_plan = None
    mayor_utilidad = float("-inf")

    for plan in lista_planes:
        planta_NCT.reiniciar_estado_contable()
        planta_ZF.reiniciar_estado_contable()

        ejecutor = cl.EjecutorPlan(plan, planta_NCT, planta_ZF, dict_precios)
        ejecutor.ejecutar()

        utilidad_aggregada = (
            planta_NCT.calcular_utilidad_operacional()
            + planta_ZF.calcular_utilidad_operacional()
        )

        if utilidad_aggregada > mayor_utilidad:
            mayor_utilidad = utilidad_aggregada
            mejor_plan = plan

    return mejor_plan, mayor_utilidad


# Función para actualizar valores y ejecutar el cálculo
def actualizar_y_calcular():
    for key, entry in entries.items():
        try:
            dict_precios_2[key] = float(entry.get())
        except ValueError:
            dict_precios_2[key] = 0  # Valor por defecto en caso de error

    lista_planes = list(itertools.product([0, 1], repeat=3))
    mejor_plan, utilidad = calcular_mejor_plan(
        lista_planes, planta_NCT, planta_ZF, dict_precios_2
    )

    resultado_var.set(f"Mejor Plan: {mejor_plan}\nUtilidad: {utilidad:.2f}")


# Crear la ventana principal
root = tk.Tk()
root.title("Modificación de Precios y Cálculo")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Crear entradas para modificar el diccionario
entries = {}
row = 0
for key, value in dict_precios_2.items():
    ttk.Label(frame, text=f"{key}:").grid(row=row, column=0, sticky=tk.W)
    entry = ttk.Entry(frame, width=10)
    entry.insert(0, value)
    entry.grid(row=row, column=1)
    entries[key] = entry
    row += 1

# Botón para ejecutar
ttk.Button(frame, text="Calcular Mejor Plan", command=actualizar_y_calcular).grid(
    row=row, column=0, columnspan=2
)

# Resultado
resultado_var = tk.StringVar()
resultado_label = ttk.Label(
    frame, textvariable=resultado_var, relief="solid", padding=5
)
resultado_label.grid(row=row + 1, column=0, columnspan=2, sticky=(tk.W, tk.E))

root.mainloop()
