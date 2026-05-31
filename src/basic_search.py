from collections import deque
from unified_planning.shortcuts import SequentialSimulator

class Nodo:
    def __init__(self, estado, padre=None, accion_aplicada=None, profundidad=0):
        """
        Representa un nodo en el árbol de búsqueda.
        
        :param estado: El estado del tablero en este nodo (formato de UP).
        :param padre: Referencia al nodo padre del que proviene.
        :param accion_aplicada: La acción instanciada que generó este estado.
        :param profundidad: Coste o nivel de profundidad en el árbol.
        """
        self.estado = estado
        self.padre = padre
        self.accion_aplicada = accion_aplicada
        self.profundidad = profundidad

    def extraer_plan(self):
        """
        Navega hacia atrás usando las referencias al padre para reconstruir 
        la lista de acciones desde el inicio hasta el objetivo.
        """
        plan = []
        nodo_actual = self
        
        while nodo_actual.accion_aplicada is not None:
            plan.append(nodo_actual.accion_aplicada)
            nodo_actual = nodo_actual.padre
        
        plan.reverse()
        return plan

def busqueda_ciega(problema, usar_bfs=True):
    """
    Ejecuta una búsqueda básica sobre un problema PDDL.
    
    :param problema: Instancia del problema cargado desde UP.
    :param usar_bfs: True para Búsqueda en Anchura (BFS), False para Profundidad (DFS).
    :return: Lista de acciones que resuelven el problema, o None si no hay solución.
    """
    
    with SequentialSimulator(problem=problema) as simulador:
        estado_inicial = simulador.get_initial_state()
        nodo_raiz = Nodo(estado=estado_inicial)
        
        if simulador.is_goal(estado_inicial):
            print("El estado inicial ya es el objetivo.")
            return []

        frontera = deque([nodo_raiz])
        visitados = set()
        visitados.add(hash_estado(estado_inicial, problema))
        
        nodos_expandidos = 0

        while frontera:
            if usar_bfs:
                nodo_actual = frontera.popleft()  # FIFO (Anchura)
            else:
                nodo_actual = frontera.pop()      # LIFO (Profundidad)

            nodos_expandidos += 1
            
            if nodos_expandidos % 50 == 0:
                print(f"Nodos expandidos: {nodos_expandidos}, Frontera: {len(frontera)}")

            acciones_aplicables = simulador.get_applicable_actions(nodo_actual.estado)

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
                
                hash_sucesor = hash_estado(estado_sucesor, problema)

                if hash_sucesor not in visitados:
                    
                    if simulador.is_goal(estado_sucesor):
                        nodo_objetivo = Nodo(
                            estado=estado_sucesor, 
                            padre=nodo_actual, 
                            accion_aplicada=accion, 
                            profundidad=nodo_actual.profundidad + 1
                        )
                        print(f"\n¡Solución encontrada! Nodos expandidos: {nodos_expandidos}")
                        print(f"Profundidad de la solución (saltos): {nodo_objetivo.profundidad}")
                        return nodo_objetivo.extraer_plan()

                    visitados.add(hash_sucesor)
                    
                    nuevo_nodo = Nodo(
                        estado=estado_sucesor, 
                        padre=nodo_actual, 
                        accion_aplicada=accion, 
                        profundidad=nodo_actual.profundidad + 1
                    )
                    frontera.append(nuevo_nodo)

        print(f"\nBúsqueda finalizada sin éxito. Nodos expandidos en total: {nodos_expandidos}")
        return None
    
def hash_estado(estado, problema):
    """
    Convierte el estado de UP en un frozenset inmutable.
    Utiliza las claves del estado inicial como 'plantilla' para preguntar
    por el valor de cada fluente, sorteando el problema de los estados delta.
    """
    fluentes_activos = []
    
    for fluente in problema.initial_values.keys():
        try:
            if estado.get_value(fluente).is_true():
                fluentes_activos.append(str(fluente))
        except Exception:
            pass
            
    return frozenset(fluentes_activos)