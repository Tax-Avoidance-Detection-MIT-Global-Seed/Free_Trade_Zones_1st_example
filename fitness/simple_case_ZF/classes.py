#! Script para realizar la calculadora

from typing import List, Dict, Optional, Tuple
from abc import ABC, abstractmethod


class Account:
    """
    Clase para generar las cuentas y registrarlas
    """

    def __init__(self, name: str, tipo: int):
        self.historial = {}  # Diccionario vacío para el historial
        self.contador_transacciones = 0  # Contador de transacciones
        self.name = name
        self.tipo = tipo

    def registrar_transaccion(self, debe=0, haber=0) -> None:
        if not isinstance(debe, (int, float)) or not isinstance(haber, (int, float)):
            raise ValueError("Los valores de 'debe' y 'haber' deben ser números.")

        # Aumenta el contador de transacciones
        self.contador_transacciones += 1

        # Crea un registro de la transacción
        transaccion = {"debe": debe, "haber": haber}

        # Añade la transacción al historial
        self.historial[self.contador_transacciones] = transaccion

    def mostrar_historial(self) -> None:
        return self.historial

    def calcular_totales(self) -> dict:
        total_debe = self.debe
        total_haber = self.haber
        neto = total_haber - total_debe

        if neto > 0:
            saldo = {"haber": neto}
        elif neto < 0:
            saldo = {"debe": -neto}
        else:
            saldo = "Saldo neto: 0 (Debe y Haber son iguales)"

        return {"Debe": total_debe, "Haber": total_haber, "Neto": saldo}

    def saldo_neto(self) -> dict:
        neto = self.haber - self.debe

        if neto > 0:
            saldo = {"haber": neto}
        elif neto < 0:
            saldo = {"debe": -neto}
        else:
            saldo = {"debe": 0, "haber": 0}

        return saldo

    @property
    def debe(self) -> float:
        """
        Propiedad que devuelve la suma total de los valores de "debe" en el historial de transacciones.

        :return: Suma total de los valores de "debe".
        :rtype: float
        """
        return sum(transaccion["debe"] for transaccion in self.historial.values())

    @property
    def haber(self) -> float:
        return sum(transaccion["haber"] for transaccion in self.historial.values())


### --------------------- Libro Contable


class LibroContable:
    def __init__(self, plantillas_cuentas: Dict, plantillas_transacciones: Dict):
        self.plantillas_transacciones = plantillas_transacciones
        self.cuentas = {}

        for codigo, plantilla in plantillas_cuentas.items():
            cuenta_nombre = plantilla["cuenta"]
            codigo_tipo_cuenta = plantilla["codigo_tipo_cuenta"]
            # Creamos una nueva instancia de Account para cada cuenta del agente
            self.cuentas[codigo] = Account(name=cuenta_nombre, tipo=codigo_tipo_cuenta)

    def get_account_by_name(self, account_name: str) -> Optional["Account"]:
        """
        Obtiene una cuenta por su nombre.

        :param account_name: El nombre de la cuenta a buscar.
        :return: La cuenta encontrada o None si no existe.
        """
        for cuenta in self.cuentas.values():
            if cuenta.name == account_name:
                return cuenta
        return None

    def get_account_by_code(self, account_code: str) -> Optional["Account"]:
        """
        Obtiene una cuenta por su código.

        :param account_code: El código de la cuenta a buscar.
        :return: La cuenta encontrada o None si no existe.
        """
        return self.cuentas.get(int(account_code), None)

    def debitar_cuenta(self, cuenta_codigo: str, monto: float):
        """
        Debita una cuenta del agente.

        :param cuenta_codigo: Código de la cuenta a debitar.
        :param monto: Monto a debitar de la cuenta.
        """
        cuenta = self.get_account_by_code(cuenta_codigo)
        cuenta.registrar_transaccion(monto, 0)

    def acreditar_cuenta(self, cuenta_codigo: str, monto: float):
        """
        Acredita una cuenta del agente.

        :param cuenta_codigo: Código de la cuenta a acreditar.
        """
        cuenta = self.get_account_by_code(cuenta_codigo)
        cuenta.registrar_transaccion(0, monto)

    def calcular_utilidad_operacional(self, tasa_impuesto: float) -> str:
        """
        Calcula la utilidad operacional y genera un estado de resultados.

        :param tasa_impuesto: Tasa porcentual de impuesto (por ejemplo, 0.3 para 30%).
        :return: Estado de resultados en formato de texto.
        """
        total_ingresos = 0
        total_costos = 0

        # Filtra las cuentas por tipo de una vez
        cuentas_tipo_4 = [
            cuenta for cuenta in self.cuentas.values() if cuenta.tipo == 4
        ]
        cuentas_tipo_6 = [
            cuenta for cuenta in self.cuentas.values() if cuenta.tipo == 6
        ]

        # Suma los ingresos y costos
        total_ingresos = sum(cuenta.haber - cuenta.debe for cuenta in cuentas_tipo_4)
        total_costos = sum(cuenta.debe - cuenta.haber for cuenta in cuentas_tipo_6)

        ### Determina las cantidades de interés y utilidad neta
        utilidad_bruta = total_ingresos - total_costos

        impuesto = utilidad_bruta * tasa_impuesto

        utilidad_neta = utilidad_bruta - impuesto

        return utilidad_neta  # Devuelve el estado_resultados

    def estado_resultados(self, tasa_impuesto: float) -> str:
        """
        Calcula la utilidad operacional y genera un estado de resultados.

        :param tasa_impuesto: Tasa porcentual de impuesto (por ejemplo, 0.3 para 30%).
        :return: Estado de resultados en formato de texto.
        """
        total_ingresos = 0
        total_costos = 0

        # Filtra las cuentas por tipo de una vez
        cuentas_tipo_4 = [
            cuenta for cuenta in self.cuentas.values() if cuenta.tipo == 4
        ]
        cuentas_tipo_6 = [
            cuenta for cuenta in self.cuentas.values() if cuenta.tipo == 6
        ]

        # Suma los ingresos y costos
        total_ingresos = sum(cuenta.haber - cuenta.debe for cuenta in cuentas_tipo_4)
        total_costos = sum(cuenta.debe - cuenta.haber for cuenta in cuentas_tipo_6)

        ### Determina las cantidades de interés y utilidad neta
        utilidad_bruta = total_ingresos - total_costos
        if utilidad_bruta < 0:
            impuesto = 0
        else:
            impuesto = utilidad_bruta * tasa_impuesto

        utilidad_neta = utilidad_bruta - impuesto

        # Generar el estado de resultados
        estado_resultados = (
            f"Ingresos Totales: {total_ingresos}\n"
            f"Costos Totales: {total_costos}\n"
            f"Utilidad Bruta: {utilidad_bruta}\n"
            f"Impuesto ({tasa_impuesto * 100}%): {impuesto}\n"
            f"Utilidad Neta: {utilidad_neta}\n"
        )

        return print(estado_resultados)  # Devuelve el estado_resultados


### ---------------------- Clase Good ------------------------------


class Good:
    """
    Clase abstracta base para los bienes.
    Permite añadir precio, tarifa del IVA, arancel e insumos necesarios para producir el bien.
    """

    def __init__(
        self,
        name: str,
        price: float,
        insumos: Dict[str, float] = None,
        tipo_bien: str = None,
    ):
        """
        Inicializa un nuevo bien.

        :param name: Nombre del bien.
        :param price: Precio base del bien.
        :param insumos: Diccionario de insumos necesarios para producir el bien.
                        Las claves son los nombres de otros bienes y los valores son las cantidades requeridas.
        :param tipo_bien: Tipo del bien ("materia prima", "intermedio", "final").
        """
        self.name = name
        self.price = price
        self.insumos = insumos if insumos is not None else {}
        self.tipo_bien = tipo_bien

    def asignar_tipo_bien(self, bienes_dict, usados_como_insumo):
        """
        Asigna el tipo de bien basado en sus insumos y si es insumo de otros bienes.

        :param bienes_dict: Diccionario de todos los bienes {nombre: objeto bien}.
        :param usados_como_insumo: Diccionario {nombre_bien: [bienes_que_lo_usan]}.
        """
        tiene_insumos = len(self.insumos) > 0
        es_insumo = self.name in usados_como_insumo

        if tiene_insumos and es_insumo:
            self.tipo_bien = "bien_intermedio"
        elif not tiene_insumos and es_insumo:
            self.tipo_bien = "materia_prima"
        elif tiene_insumos and not es_insumo:
            self.tipo_bien = "bien_final"
        else:
            self.tipo_bien = "independiente"  # No tiene insumos y no es insumo de nadie

    def __repr__(self):
        return f"{self.name} ({self.tipo_bien})"

    def cambiar_tipo_bien(self, nuevo_tipo_bien: str):
        self.tipo_bien = nuevo_tipo_bien


class MateriaPrima(Good):
    def __init__(self, name: str, price: float, insumos: Dict[str, float] = None):
        super().__init__(name, price, insumos, "materia_prima")


class BienIntermedio(Good):
    def __init__(self, name: str, price: float, insumos: Dict[str, float] = None):
        super().__init__(name, price, insumos, "bien_intermedio")


class BienFinal(Good):
    def __init__(self, name: str, price: float, insumos: Dict[str, float] = None):
        super().__init__(name, price, insumos, "bien_final")


# -------------- Clase Agente ----------------

#  TODO: Agregar la tasa del impuesto en el init

class Agent(ABC):
    """
    Clase base abstracta para los agentes.
    """

    def __init__(
        self,
        nombre: str,
        plantillas_cuentas: Dict,
        plantillas_transacciones: Dict,
    ):
        """
        Inicializa una nueva instancia de Agent.

        :param nombre: El nombre del agente.
        :param plantillas_cuentas: Un diccionario que contiene las plantillas de cuentas
                                   que se usarán para crear instancias de Account para el agente.
        :param plantillas_transacciones: Un diccionario que contiene las plantillas de transacciones
                                         que se usarán para crear instancias de Transaction para el agente.
        """
        self.nombre = nombre
        self.type = self.get_type()  # Establece el tipo según la subclase
        self.plantilla_cuentas = plantillas_cuentas
        self.plantilla_transacciones = plantillas_transacciones
        # Crear el libro contable del agente
        self.libro_contable = LibroContable(
            plantillas_cuentas, plantillas_transacciones
        )

    def reiniciar_estado_contable(self):
        self.libro_contable = LibroContable(
            self.plantilla_cuentas, self.plantilla_transacciones
        )

    @abstractmethod
    def get_type(self) -> str:
        """
        Método abstracto para obtener el tipo de empresa.
        Debe ser implementado por las subclases.
        """
        pass

    def __repr__(self):
        return f"{self.type} {self.nombre}"

    def __str__(self):
        return f"{self.type} {self.nombre}"


# Subclase para empresas ZF
class ZF(Agent):
    def get_tasa_impuesto(self):
        return 0.2

    def get_type(self) -> str:
        return "ZF"

    def calcular_utilidad_operacional(self):
        return self.libro_contable.calcular_utilidad_operacional(
            self.get_tasa_impuesto()
        )

    def generar_estado_resultados(self):
        return self.libro_contable.estado_resultados(self.get_tasa_impuesto())


# Subclase para empresas NCT
class NCT(Agent):
    def get_tasa_impuesto(self):
        return 0.35

    def get_type(self) -> str:
        return "NCT"

    def calcular_utilidad_operacional(self):
        return self.libro_contable.calcular_utilidad_operacional(
            self.get_tasa_impuesto()
        )

    def generar_estado_resultados(self):
        return self.libro_contable.estado_resultados(self.get_tasa_impuesto())


class Market(Agent):
    def get_type(self) -> str:
        return "MKT"


# ------------------------------------ Clase Flow --------------------------------------------


class Flow:
    def __init__(
        self, name: str, owner, precio_venta: float = 0, ultimo_costo: float = 0
    ):
        self.name = name
        self.owner = owner
        self.precio_venta = precio_venta
        self.ultimo_costo = ultimo_costo
        self.historial = []  # Lista vacía para el historial
        self.guardar_en_historial()  # Guarda el estado inicial en el historial

    def guardar_en_historial(self):
        estado = {
            "owner": self.owner,
            "precio_venta": self.precio_venta,
            "ultimo_costo": self.ultimo_costo,
        }
        self.historial.append(estado)

    def actualizar_precio_venta(self, nuevo_precio_venta: float):
        self.precio_venta = nuevo_precio_venta
        self.guardar_en_historial()

    def actualizar_ultimo_costo(self, nuevo_ultimo_costo: float):
        self.ultimo_costo = nuevo_ultimo_costo
        self.guardar_en_historial()

    def actualizar_owner(self, nuevo_owner):
        self.owner = nuevo_owner
        self.guardar_en_historial()


# ------------------------------------- Clase Transaccion ------------------------------------


### Funcion auxiliar para debugging
def obtener_plantilla_compra(comprador: Agent, tipo_bien) -> dict:
    """
    Obtiene la plantilla de compra para un tipo de bien en el libro contable del comprador.

    Args:
        comprador (Agent): El agente comprador con un libro contable que contiene plantillas.
        tipo_bien (str): El tipo de bien para el cual se busca la plantilla de compra.

    Returns:
        dict: La plantilla de compra para el tipo de bien.

    Raises:
        ValueError: Si no se encuentra una plantilla de compra para el tipo de bien.
    """
    try:
        plantilla = comprador.libro_contable.plantillas_transacciones.get(
            tipo_bien, {}
        ).get("compra", {})
        if not plantilla:
            raise ValueError(
                f"No se encontró una plantilla de compra para el tipo de bien '{tipo_bien}'"
            )
        return plantilla
    except Exception as e:
        # Agregar un punto de depuración aquí
        print("Error al obtener la plantilla de compra")
        print(f"Comprador: {comprador}")
        print(f"Tipo de bien: {tipo_bien}")
        print(f"Libro contable: {comprador.libro_contable}")
        print(
            f"Plantillas de transacciones: {comprador.libro_contable.plantillas_transacciones}"
        )
        raise e


def obtener_plantilla_venta(vendedor: Agent, tipo_bien) -> dict:
    """
    Obtiene la plantilla de compra para un tipo de bien en el libro contable del comprador.

    Args:
        comprador (Agent): El agente comprador con un libro contable que contiene plantillas.
        tipo_bien (str): El tipo de bien para el cual se busca la plantilla de compra.

    Returns:
        dict: La plantilla de compra para el tipo de bien.

    Raises:
        ValueError: Si no se encuentra una plantilla de compra para el tipo de bien.
    """
    try:
        plantilla = vendedor.libro_contable.plantillas_transacciones.get(
            tipo_bien, {}
        ).get("venta", {})
        if not plantilla:
            raise ValueError(
                f"No se encontró una plantilla de compra para el tipo de bien '{tipo_bien}'"
            )
        return plantilla
    except Exception as e:
        # Agregar un punto de depuración aquí
        print("Error al obtener la plantilla de compra")
        print(f"Comprador: {vendedor}")
        print(f"Tipo de bien: {tipo_bien}")
        print(f"Libro contable: {vendedor.libro_contable}")
        print(
            f"Plantillas de transacciones: {vendedor.libro_contable.plantillas_transacciones}"
        )
        raise e


def obtener_plantilla_produccion(productor: Agent, tipo_bien) -> dict:
    """
    Obtiene la plantilla de compra para un tipo de bien en el libro contable del comprador.

    Args:
        comprador (Agent): El agente comprador con un libro contable que contiene plantillas.
        tipo_bien (str): El tipo de bien para el cual se busca la plantilla de compra.

    Returns:
        dict: La plantilla de compra para el tipo de bien.

    Raises:
        ValueError: Si no se encuentra una plantilla de compra para el tipo de bien.
    """
    try:
        plantilla = productor.libro_contable.plantillas_transacciones.get(
            tipo_bien, {}
        ).get("produccion", {})
        if not plantilla:
            raise ValueError(
                f"No se encontró una plantilla de compra para el tipo de bien '{tipo_bien}'"
            )
        return plantilla
    except Exception as e:
        # Agregar un punto de depuración aquí
        print("Error al obtener la plantilla de compra")
        print(f"Comprador: {productor}")
        print(f"Tipo de bien: {productor}")
        print(f"Libro contable: {productor.libro_contable}")
        print(
            f"Plantillas de transacciones: {productor.libro_contable.plantillas_transacciones}"
        )
        raise e


class Transaccion:
    def __init__(
        self,
        vendedor: Agent,
        comprador: Agent,
        bien: Good,
        dict_precios_transaccion: Dict[Tuple[str, str, str], float],
    ):
        self.bien = bien
        self.vendedor = vendedor
        self.comprador = comprador
        self.dict_precios_transaccion = dict_precios_transaccion
        self.tipo_bien = bien.tipo_bien
        self.key = (
            vendedor.type,
            comprador.type,
            bien.tipo_bien,
        )

    def get_key(self):
        return self.key

    def registrar_compra(self, precio: float) -> None:
        """
        Registra una compra de un bien por parte del comprador, actualizando sus cuentas contables.
        """
        comprador = self.comprador
        tipo_bien = self.bien.tipo_bien
        # Obtener la plantilla de compra para el tipo de bien
        plantilla = obtener_plantilla_compra(comprador, tipo_bien)

        # Actualizar las cuentas del comprador según la plantilla
        for cuenta_codigo, valor_key in plantilla.get("debito", []):
            comprador.libro_contable.debitar_cuenta(cuenta_codigo, precio)

        for cuenta_codigo, valor_key in plantilla.get("credito", []):
            comprador.libro_contable.acreditar_cuenta(cuenta_codigo, precio)

    def registrar_venta(self, precio: float, costo: float) -> None:
        """
        Registra una venta de un bien por parte del vendedor, actualizando sus cuentas contables.
        """
        vendedor = self.vendedor
        tipo_bien = self.bien.tipo_bien

        # Obtener la plantilla de venta para el tipo de bien
        plantilla = obtener_plantilla_venta(vendedor, tipo_bien)

        debitos = []
        creditos = []

        # Procesar la plantilla, reemplazando 'precio' y 'costo' por los argumentos proporcionados
        for cuenta, variable in plantilla.get("debito", []):
            if variable == "precio":
                valor = precio
            elif variable == "costo":
                valor = costo
            else:
                raise ValueError(f"Variable desconocida '{variable}' en débito")

            debitos.append((cuenta, valor))

        for cuenta, variable in plantilla.get("credito", []):
            if variable == "precio":
                valor = precio
            elif variable == "costo":
                valor = costo
            else:
                raise ValueError(f"Variable desconocida '{variable}' en crédito")
            creditos.append((cuenta, valor))

        # Actualizar las cuentas del vendedor con los nuevos debitos y creditos
        # Actualizar las cuentas contables del agente
        for cuenta_codigo, valor in debitos:
            vendedor.libro_contable.debitar_cuenta(cuenta_codigo, valor)

        for cuenta_codigo, valor in creditos:
            vendedor.libro_contable.acreditar_cuenta(cuenta_codigo, valor)


# ------------------------------------- Clase Produccion ---------------------------------------


class Produccion:
    def __init__(self, agente: Agent, bien_input: Good, bien_output: Good):
        self.agente = agente
        self.bien_input = bien_input
        self.bien_output = bien_output

    def registrar_produccion(self, costo: float) -> None:
        """
        Registra una operación de producción, actualizando las cuentas contables del agente.
        """
        tipo_bien_input = self.bien_input.tipo_bien
        # tipo_bien_output = self.bien_output.tipo_bien

        # Obtener la plantilla de producción para el tipo de bien de salida
        plantilla = obtener_plantilla_produccion(self.agente, tipo_bien_input)

        # Procesar la plantilla, reemplazando 'costo' por el argumento proporcionado
        debitos = []
        creditos = []

        for cuenta_codigo, variable in plantilla.get("debito", []):
            if variable == "costo":
                valor = costo
            else:
                raise ValueError(f"Variable desconocida '{variable}' en débito")
            debitos.append((cuenta_codigo, valor))

        for cuenta_codigo, variable in plantilla.get("credito", []):
            if variable == "costo":
                valor = costo
            else:
                raise ValueError(f"Variable desconocida '{variable}' en crédito")
            creditos.append((cuenta_codigo, valor))

        # Actualizar las cuentas contables del agente
        for cuenta_codigo, valor in debitos:
            self.agente.libro_contable.debitar_cuenta(cuenta_codigo, valor)

        for cuenta_codigo, valor in creditos:
            self.agente.libro_contable.acreditar_cuenta(cuenta_codigo, valor)


# -# ------------------------------------- Clase ejecutor_plan -------------------------------------

# Funciones auxiliares


def mapear_valor(variable: str, flow: Flow):
    """
    Mapea el valor de una variable dada en el flujo de caja a su valor real.

    :param variable: El nombre de la variable a mapear (precio o costo).
    :param flow: El flujo de caja actual.
    :return: El valor mapeado de la variable (None si no se reconoce la variable).
    """
    if variable == "precio":
        return flow.precio_venta
    elif variable == "costo":
        return flow.ultimo_costo
    else:
        return None  # O puedes lanzar una excepción si la variable no es reconocida


# Funciones auxiliares


def obtener_precio_transaccion(
    key: Tuple[str, str, str],
    dict_precios_transaccion: Dict[Tuple[str, str, str], float],
) -> float:
    """
    Determina el precio de transaccion segun el diccionario de precios
    el parametro key es
    """
    precio = 0
    # Clave para acceder al diccionario de precios
    if key in dict_precios_transaccion:
        precio = dict_precios_transaccion[key]
    return precio


# Definicion de clase


class EjecutorPlan:
    def __init__(
        self,
        plan: List[int],
        planta_NCT: Agent,
        planta_ZF: Agent,
        dict_precios_transaccion: Dict[Tuple[str, str, str], float],
    ):
        """
        Inicializa un nuevo ejecutor de plan.

        :param plan: Lista de enteros que representa el plan de producción (0 o 1).
        :param planta_NCT: Instancia de la clase NCT, que representa la planta de NCT.
        :param planta_ZF: Instancia de la clase ZF, que representa la planta de ZF.
        :param dict_precios_transaccion: Diccionario con los precios de transacción.
        """
        self.plan = plan
        self.planta_NCT = planta_NCT
        self.planta_ZF = planta_ZF
        self.dict_precios_transaccion = dict_precios_transaccion
        self.mercado = Market(
            "Mercado",
            self.planta_NCT.plantilla_cuentas,
            self.planta_NCT.plantilla_transacciones,
        )
        self.flow = Flow("Flujo de Caja", self.mercado)

        self.materia_prima = MateriaPrima("materia_prima", 0)
        self.bien_intermedio = BienIntermedio("bien_intermedio", 0)
        self.bien_final = BienFinal("bien_final", 0)

        self.agentes = {0: self.planta_NCT, 1: self.planta_ZF}

    def ejecutar(self):
        """
        Ejecuta el plan de producción basado en la lista de decisiones.
        """
        agente_actual = self.comprar_materia_prima()
        agente_actual = self.producir_bien_intermedio(agente_actual)
        agente_actual = self.producir_bien_final(agente_actual)
        agente_actual = self.transferir_bien_final_a_NCT(agente_actual)
        self.vender_bien_final_al_mercado(agente_actual)

    def comprar_materia_prima(self):
        agente_destino = self.agentes[self.plan[0]]
        self.realizar_compra(self.mercado, agente_destino, self.materia_prima)
        return agente_destino

    def producir_bien_intermedio(self, agente_actual):
        agente_destino = self.agentes[self.plan[1]]
        if agente_actual != agente_destino:
            self.transferir_bien(agente_actual, agente_destino, self.materia_prima)
            agente_actual = agente_destino
        self.producir_bien(agente_actual, self.materia_prima, self.bien_intermedio)
        return agente_actual

    def producir_bien_final(self, agente_actual):
        agente_destino = self.agentes[self.plan[2]]
        if agente_actual != agente_destino:
            self.transferir_bien(agente_actual, agente_destino, self.bien_intermedio)
            agente_actual = agente_destino
        self.producir_bien(agente_actual, self.bien_intermedio, self.bien_final)
        return agente_actual

    def transferir_bien_final_a_NCT(self, agente_actual):
        if agente_actual != self.planta_NCT:
            self.transferir_bien(agente_actual, self.planta_NCT, self.bien_final)
            agente_actual = self.planta_NCT
        return agente_actual

    def vender_bien_final_al_mercado(self, agente_actual):
        self.realizar_venta(agente_actual, self.mercado, self.bien_final)

    def realizar_compra(self, agente_origen: Agent, agente_destino: Agent, bien: Good):
        transaccion = Transaccion(
            agente_origen, agente_destino, bien, self.dict_precios_transaccion
        )
        precio = self.obtener_precio_transaccion(transaccion.get_key())
        transaccion.registrar_compra(precio)
        self.actualizar_flow(agente_destino, precio)

    def transferir_bien(self, agente_origen, agente_destino, bien):
        transaccion = Transaccion(
            agente_origen, agente_destino, bien, self.dict_precios_transaccion
        )
        precio = self.obtener_precio_transaccion(
            transaccion.get_key(),
        )

        # Actualizar el precio de venta del flow
        self.flow.actualizar_precio_venta(precio)

        # Registrar la compra con el nuevo precio para el comprador
        transaccion.registrar_compra(self.flow.precio_venta)

        # Registrar la venta con el nuevo precio de venta y el costo anterior para el vendedor
        transaccion.registrar_venta(self.flow.precio_venta, self.flow.ultimo_costo)

        # Actualizar el owner del flow
        self.flow.actualizar_owner(agente_destino)

        # Actualizar el último costo del flow con el precio de venta
        self.flow.actualizar_ultimo_costo(self.flow.precio_venta)

    def producir_bien(self, agente, bien_entrada, bien_salida):
        produccion = Produccion(agente, bien_entrada, bien_salida)
        produccion.registrar_produccion(self.flow.ultimo_costo)

    def realizar_venta(self, agente_origen, agente_destino, bien):
        transaccion = Transaccion(
            agente_origen, agente_destino, bien, self.dict_precios_transaccion
        )
        precio = self.obtener_precio_transaccion(transaccion.get_key())
        costo = self.flow.ultimo_costo
        transaccion.registrar_venta(precio, costo)

    def obtener_precio_transaccion(self, llave):
        return obtener_precio_transaccion(llave, self.dict_precios_transaccion)

    def actualizar_flow(self, agente_destino, precio):
        self.flow.actualizar_owner(agente_destino)
        self.flow.actualizar_precio_venta(precio)
        self.flow.actualizar_ultimo_costo(precio)
