from collections import deque
from unified_planning.shortcuts import SequentialSimulator
from src.helpers import (
    Nodo,
    filtrar_fluentes_relevantes,
    extraer_adyacencias,
    generar_movimientos,
    hash_estado,
)


def busqueda_ciega(problema, usar_bfs=True, max_profundidad=None):
    """
    Ejecuta una busqueda basica (BFS o DFS) sobre un problema PDDL de Senku.
    Explora el arbol de juego sistematicamente expandiendo nodos y detectando
    estados repetidos mediante un conjunto de visitados.

    :param problema: Instancia del problema cargado desde UP.
    :param usar_bfs: True para busqueda en anchura (BFS), False para profundidad (DFS).
    :param max_profundidad: Limite de profundidad (None = sin limite).
    :return: Lista de acciones que resuelven el problema, o None si no hay solucion.
    """
    cached_keys = filtrar_fluentes_relevantes(problema.initial_values)
    adyacencias = extraer_adyacencias(problema.initial_values)
    accion_saltar = problema.action('saltar')

    with SequentialSimulator(problem=problema) as simulador:
        estado_inicial = simulador.get_initial_state()
        nodo_raiz = Nodo(estado=estado_inicial)

        if simulador.is_goal(estado_inicial):
            print("El estado inicial ya es el objetivo.")
            return []

        frontera = deque([nodo_raiz])
        visitados = set()
        visitados.add(hash_estado(estado_inicial, cached_keys))

        nodos_expandidos = 0

        while frontera:
            if usar_bfs:
                nodo_actual = frontera.popleft()
            else:
                nodo_actual = frontera.pop()

            nodos_expandidos += 1

            if nodos_expandidos % 50 == 0:
                print(f"Nodos expandidos: {nodos_expandidos}, Frontera: {len(frontera)}")

            if max_profundidad is not None and nodo_actual.profundidad >= max_profundidad:
                continue

            acciones_aplicables = generar_movimientos(
                adyacencias, accion_saltar, cached_keys, nodo_actual.estado
            )

            for accion in acciones_aplicables:
                if hasattr(accion, 'action') and hasattr(accion, 'actual_parameters'):
                    act = accion.action
                    params = accion.actual_parameters
                elif isinstance(accion, tuple):
                    act = accion[0]
                    params = accion[1]
                else:
                    continue

                estado_sucesor = simulador.apply(nodo_actual.estado, act, params)

                if estado_sucesor is None:
                    continue

                hash_sucesor = hash_estado(estado_sucesor, cached_keys)

                if hash_sucesor not in visitados:
                    if simulador.is_goal(estado_sucesor):
                        nodo_objetivo = Nodo(
                            estado=estado_sucesor,
                            padre=nodo_actual,
                            accion_aplicada=accion,
                            profundidad=nodo_actual.profundidad + 1
                        )
                        print(f"\nSolucion encontrada! Nodos expandidos: {nodos_expandidos}")
                        print(f"Profundidad de la solucion (saltos): {nodo_objetivo.profundidad}")
                        return nodo_objetivo.extraer_plan()

                    visitados.add(hash_sucesor)

                    nuevo_nodo = Nodo(
                        estado=estado_sucesor,
                        padre=nodo_actual,
                        accion_aplicada=accion,
                        profundidad=nodo_actual.profundidad + 1
                    )
                    frontera.append(nuevo_nodo)

        print(f"\nBusqueda finalizada sin exito. Nodos expandidos en total: {nodos_expandidos}")
        return None
