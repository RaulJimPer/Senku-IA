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

def _filtrar_fluentes_relevantes(initial_values):
    """
    Filtra solo los fluentes que pueden cambiar durante la ejecución
    (pieza y vacio), ignorando adyacente que es estático.
    Retorna lista de claves.
    """
    return [k for k in initial_values.keys()
            if k.fluent().name in ('pieza', 'vacio')]

def _extraer_adyacencias(initial_values):
    """
    Extrae todos los triples (origen, intermedia, destino) del predicado
    adyacente que están definidos en el estado inicial.
    Devuelve una lista de tuplas (origen, intermedia, destino).
    """
    adyacencias = []
    for k, v in initial_values.items():
        if k.fluent().name == 'adyacente' and v.is_true():
            adyacencias.append(tuple(k.args))
    return adyacencias

def _generar_movimientos(adyacencias, accion_saltar, cached_keys, estado):
    """
    Genera los movimientos válidos para un estado dado sin usar el
    grounder del simulador (que es muy lento).
    
    :param adyacencias: Lista de tuplas (origen, intermedia, destino)
    :param accion_saltar: Objeto Action de UP para saltar
    :param cached_keys: Lista de fluentes relevantes (pieza/vacio)
    :param estado: Estado actual del simulador
    :return: Lista de ActionInstance válidas
    """
    # Construir conjunto rápido de piezas y vacíos
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

def busqueda_ciega(problema, usar_bfs=True, max_profundidad=None):
    """
    Ejecuta una búsqueda básica sobre un problema PDDL.
    
    :param problema: Instancia del problema cargado desde UP.
    :param usar_bfs: True para Búsqueda en Anchura (BFS), False para Profundidad (DFS).
    :param max_profundidad: Límite de profundidad (None = sin límite).
    :return: Lista de acciones que resuelven el problema, o None si no hay solución.
    """
    
    cached_keys = _filtrar_fluentes_relevantes(problema.initial_values)
    adyacencias = _extraer_adyacencias(problema.initial_values)
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
                nodo_actual = frontera.popleft()  # FIFO (Anchura)
            else:
                nodo_actual = frontera.pop()      # LIFO (Profundidad)

            nodos_expandidos += 1
            
            if nodos_expandidos % 50 == 0:
                print(f"Nodos expandidos: {nodos_expandidos}, Frontera: {len(frontera)}")
            
            if max_profundidad is not None and nodo_actual.profundidad >= max_profundidad:
                continue

            acciones_aplicables = _generar_movimientos(
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
    
def hash_estado(estado, cached_keys):
    """
    Convierte el estado de UP en un frozenset inmutable.
    Recibe las claves de fluentes ya extraídas (cached) para evitar
    iterar sobre problema.initial_values.keys() en cada llamada.
    """
    fluentes_activos = []
    
    for fluente in cached_keys:
        try:
            if estado.get_value(fluente).is_true():
                fluentes_activos.append(str(fluente))
        except Exception:
            pass
            
    return frozenset(fluentes_activos)