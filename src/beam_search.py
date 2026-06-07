from unified_planning.shortcuts import SequentialSimulator
from src.helpers import (
    Nodo,
    filtrar_fluentes_relevantes,
    extraer_adyacencias,
    generar_movimientos,
    hash_estado,
)
from src.heuristic import heuristica_senku


def busqueda_haz(problema, tamano_haz=50, max_profundidad=None, variante_pagoda=1):
    """
    Ejecuta el algoritmo Beam Search (Busqueda en Haz) sobre un problema PDDL.
    En cada nivel del arbol genera todos los sucesores de los nodos actuales,
    los ordena por la heuristica pagoda y conserva solo los `tamano_haz` mejores.
    El proceso se repite hasta encontrar el objetivo o agotar el espacio de busqueda.

    :param problema: Instancia del problema cargado desde UP.
    :param tamano_haz: Numero maximo de nodos a conservar por nivel (anchura del haz).
    :param max_profundidad: Limite de profundidad (None = sin limite).
    :param variante_pagoda: Variante de la funcion pagoda para la heuristica (1, 2 o 3).
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

        frontera = [nodo_raiz]
        visitados = set()
        visitados.add(hash_estado(estado_inicial, cached_keys))

        nodos_expandidos = 0
        nivel = 0

        while frontera:
            print(f"Nivel: {nivel}, Nodos en este nivel: {len(frontera)}, "
                  f"Nodos expandidos hasta ahora: {nodos_expandidos}")
            if max_profundidad is not None and nivel >= max_profundidad:
                break

            sucesores = []

            for nodo_actual in frontera:
                nodos_expandidos += 1

                acciones_aplicables = generar_movimientos(
                    adyacencias, accion_saltar, cached_keys, nodo_actual.estado
                )

                for accion in acciones_aplicables:
                    if hasattr(accion, 'action'):
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
                            print(f"\nSolucion encontrada con Beam Search! "
                                  f"Nodos expandidos total: {nodos_expandidos}")
                            print(f"Profundidad de la solucion (saltos): {nodo_objetivo.profundidad}")
                            return nodo_objetivo.extraer_plan()

                        visitados.add(hash_sucesor)

                        nuevo_nodo = Nodo(
                            estado=estado_sucesor,
                            padre=nodo_actual,
                            accion_aplicada=accion,
                            profundidad=nodo_actual.profundidad + 1
                        )
                        sucesores.append(nuevo_nodo)

            sucesores.sort(key=lambda n: heuristica_senku(n.estado, cached_keys, variante_pagoda))

            frontera = sucesores[:tamano_haz]
            nivel += 1

        print(f"\nBusqueda (Haz) finalizada sin exito. "
              f"Nodos expandidos total: {nodos_expandidos}")
        return None
