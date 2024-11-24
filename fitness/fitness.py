"""Module for the fitness functions. A fitness function serves as an interface between
the engagement environment and the search heuristic. It provides the engagement
environment with the actions. It computes a fitness score based on the measurements
from the engagement environment.
"""

import ast
import json
from typing import List, Dict, Any, Tuple, Callable
from pathlib import Path

from heuristics.donkey_ge import Individual, DEFAULT_FITNESS, FitnessFunction
from util import utils

from simple_case_ZF.accounting_templates import plantillas_contables_1, dict_precios_2

from simple_case_ZF.utils import cargar_plantillas_cuentas

import simple_case_ZF.classes as cl

PATH = str((Path(__file__).resolve()).parent)
excel_file_name = r"/directorio_cuentas.xlsx"

plantilla_cuentas = cargar_plantillas_cuentas(PATH + excel_file_name)


class SimpleSum(FitnessFunction):
    """
    SimpleSum fitness function

    Attributes:
        n_iterations: Number of iterations of the Prisoners Dilemma
    """

    def __init__(self, param: Dict[str, Any]) -> None:
        """Initialize object"""
        self.dct = ast.literal_eval(param["pagos"])

    def __call__(self, fcn_str: str, cache: Dict[str, float]) -> float:
        """Returns the sum of the phenotype (fcn_str)."""
        key: str = "{}".format(fcn_str)
        if key in cache:
            fitness: float = cache[key]
        else:
            lst = ast.literal_eval(fcn_str)
            fitness = self.get_fitness(lst)
            cache[key] = fitness

        return fitness

    def get_fitness(self, lst: List[str]) -> float:
        """Fitness is the sum of the elements in lst"""
        fitness = 0
        for enterprise in lst:
            fitness += self.dct[enterprise]

        return fitness


if __name__ == "__main__":
    pass


"""




### Instanciar Agentes de NCT y ZF
planta_NCT = cl.NCT("NCT", plantilla_1, plantillas_contables_1)
planta_ZF = cl.ZF("ZF", plantilla_1, plantillas_contables_1)


lista_planes = list(itertools.product([0, 1], repeat=3))


ejecutor = cl.EjecutorPlan(plan, planta_NCT, planta_ZF, dict_precios_2)
ejecutor.ejecutar()

u1 = planta_NCT.generar_estado_resultados()

u2 = planta_ZF.generar_estado_resultados()

W = (
     planta_NCT.calcular_utilidad_operacional()
     + planta_ZF.calcular_utilidad_operacional()) 

"""


class Profit(FitnessFunction):
    def __init__(self, param: Dict[str, Any]) -> None:
        self.plantillas_cuentas = plantilla_cuentas
        self.plantillas_asientos_contables = plantillas_contables_1
        self.dict_precios = dict_precios_2
        self.phenotype_conversion = param["phenotype_conversion"]

    def __call__(self, fcn_str: str, cache: Dict[str, float]) -> float:
        """Returns the sum of the phenotype (fcn_str)."""
        key: str = "{}".format(fcn_str)
        if key in cache:
            fitness: float = cache[key]
        else:
            lst = ast.literal_eval(fcn_str)
            #! TODO evaluar si lst es requiere una conversion de los strings de NCT a los planes en forma [000]
            lista = []

            for enterpise in lst:
                lista.append(self.phenotype_conversion[enterpise])

            fitness = self.get_profit(lista)
            cache[key] = fitness

        return fitness

    def get_profit(self, lst: List[str]) -> float:
        planta_NCT = cl.NCT(
            "NCT", self.plantillas_cuentas, self.plantillas_asientos_contables
        )
        planta_ZF = cl.ZF(
            "ZF", self.plantillas_cuentas, self.plantillas_asientos_contables
        )
        ejecutor = cl.EjecutorPlan(lst, planta_NCT, planta_ZF, self.dict_precios)
        ejecutor.ejecutar()

        u1 = planta_NCT.calcular_utilidad_operacional()

        u2 = planta_ZF.calcular_utilidad_operacional()

        W = u1 + u2

        return W
