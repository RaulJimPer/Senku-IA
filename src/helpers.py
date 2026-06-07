from collections import deque
from unified_planning.shortcuts import SequentialSimulator


class Nodo:
    def __init__(self, estado, padre=None, accion_aplicada=None, profundidad=0):
        """
        Representa un nodo en el arbol de busqueda.

        :param estado: Estado del tablero en este nodo (formato UP).
        :param padre: Nodo padre del que proviene.
        :param accion_aplicada: Accion instanciada que genero este estado.
        :param profundidad: Profundidad o nivel en el arbol.
        """
        self.estado = estado
        self.padre = padre
        self.accion_aplicada = accion_aplicada
        self.profundidad = profundidad

    def extraer_plan(self):
        """
        Reconstruye la secuencia de acciones desde la raiz hasta este nodo
        recorriendo hacia atras las referencias al padre.

        :return: Lista de acciones desde el inicio hasta el objetivo.
        """
        plan = []
        nodo_actual = self
        while nodo_actual.accion_aplicada is not None:
            plan.append(nodo_actual.accion_aplicada)
            nodo_actual = nodo_actual.padre
        plan.reverse()
        return plan


def filtrar_fluentes_relevantes(initial_values):
    """
    Filtra solo los fluentes que cambian durante la ejecucion (pieza y vacio),
    ignorando el predicado estatico adyacente.

    :param initial_values: Diccionario de fluentes iniciales del problema.
    :return: Lista de claves de fluentes relevantes.
    """
    return [k for k in initial_values.keys()
            if k.fluent().name in ('pieza', 'vacio')]


def extraer_adyacencias(initial_values):
    """
    Extrae todos los triples (origen, intermedia, destino) del predicado
    adyacente definidos en el estado inicial.

    :param initial_values: Diccionario de fluentes iniciales del problema.
    :return: Lista de tuplas (origen, intermedia, destino).
    """
    adyacencias = []
    for k, v in initial_values.items():
        if k.fluent().name == 'adyacente' and v.is_true():
            adyacencias.append(tuple(k.args))
    return adyacencias


def generar_movimientos(adyacencias, accion_saltar, cached_keys, estado):
    """
    Genera los movimientos validos desde un estado sin usar el grounder
    del simulador, comprobando directamente las adyacencias contra las
    piezas y huecos actuales.

    :param adyacencias: Lista de tuplas (origen, intermedia, destino).
    :param accion_saltar: Objeto Action de UP para saltar.
    :param cached_keys: Lista de fluentes relevantes (pieza/vacio).
    :param estado: Estado actual del simulador UP.
    :return: Lista de tuplas (accion, parametros) validas.
    """
    piezas = set()
    vacios = set()
    for fluente in cached_keys:
        try:
            val = estado.get_value(fluente)
            if val.is_true():
                name = fluente.fluent().name
                obj = fluente.args[0]
                if name == 'pieza':
                    piezas.add(obj)
                elif name == 'vacio':
                    vacios.add(obj)
        except Exception:
            pass

    movimientos = []
    for origen, intermedia, destino in adyacencias:
        if origen in piezas and intermedia in piezas and destino in vacios:
            movimientos.append((accion_saltar, (origen, intermedia, destino)))
    return movimientos


def hash_estado(estado, cached_keys):
    """
    Convierte un estado de UP en un frozenset inmutable para su uso en el
    conjunto de visitados, considerando solo los fluentes relevantes.

    :param estado: Estado del simulador UP.
    :param cached_keys: Lista de fluentes relevantes (pieza/vacio).
    :return: Frozenset con los fluentes activos del estado.
    """
    fluentes_activos = []
    for fluente in cached_keys:
        try:
            if estado.get_value(fluente).is_true():
                fluentes_activos.append(str(fluente))
        except Exception:
            pass
    return frozenset(fluentes_activos)
