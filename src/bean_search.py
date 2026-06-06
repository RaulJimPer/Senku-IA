from src.basic_search import (
    Nodo, 
    _filtrar_fluentes_relevantes, 
    _extraer_adyacencias, 
    _generar_movimientos, 
    hash_estado
)

def heuristica_senku(estado, cached_keys):
    """
    Heurística Pagoda para Senku (una ponderación por posición).
    Se asigna un peso fijo a cada casilla (pagoda weights). La heurística
    es la suma de los pesos de las casillas ocupadas por piezas. Menor
    valor = estado más cercano al objetivo (pieza en el centro).
    """
    # Matriz de pesos para tablero 7x7 (índices 1..7). Zonas no válidas
    # (esquinas) se mantienen a 0. Valores elegidos simétricamente.
    pagoda_matrix = [
        [0, 0, 3, 3, 3, 0, 0],
        [0, 2, 3, 3, 3, 2, 0],
        [3, 3, 4, 4, 4, 3, 3],
        [3, 3, 4, 0, 4, 3, 3],
        [3, 3, 4, 4, 4, 3, 3],
        [0, 2, 3, 3, 3, 2, 0],
        [0, 0, 3, 3, 3, 0, 0],
    ]

    score = 0
    for fluente in cached_keys:
        try:
            val = estado.get_value(fluente)
            if val.is_true() and fluente.fluent().name == 'pieza':
                p_name = str(fluente.args[0])
                if p_name.startswith('c') and len(p_name) >= 3:
                    try:
                        x = int(p_name[1])
                        y = int(p_name[2])
                        if 1 <= x <= 7 and 1 <= y <= 7:
                            score += pagoda_matrix[x-1][y-1]
                    except ValueError:
                        pass
        except Exception:
            pass

    return score

def busqueda_haz(problema, tamano_haz=50, max_profundidad=None):
    """
    Ejecuta el algoritmo Beam Search (Búsqueda en Haz) sobre un problema PDDL.
    
    :param problema: Instancia del problema cargado desde UP.
    :param tamano_haz: Número máximo de nodos a conservar por nivel (W).
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

        frontera = [nodo_raiz]
        visitados = set()
        visitados.add(hash_estado(estado_inicial, cached_keys))
        
        nodos_expandidos = 0
        nivel = 0

        while frontera:
            print(f"Nivel: {nivel}, Nodos en este nivel: {len(frontera)}, Nodos expandidos hasta ahora: {nodos_expandidos}")
            if max_profundidad is not None and nivel >= max_profundidad:
                break
                
            sucesores = []
            
            for nodo_actual in frontera:
                nodos_expandidos += 1
                
                acciones_aplicables = _generar_movimientos(
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
                            print(f"\n¡Solución encontrada con Beam Search! Nodos expandidos total: {nodos_expandidos}")
                            print(f"Profundidad de la solución (saltos): {nodo_objetivo.profundidad}")
                            return nodo_objetivo.extraer_plan()

                        visitados.add(hash_sucesor)
                        
                        nuevo_nodo = Nodo(
                            estado=estado_sucesor, 
                            padre=nodo_actual, 
                            accion_aplicada=accion, 
                            profundidad=nodo_actual.profundidad + 1
                        )
                        sucesores.append(nuevo_nodo)
            
            sucesores.sort(key=lambda n: heuristica_senku(n.estado, cached_keys))
            
            frontera = sucesores[:tamano_haz]
            nivel += 1

        print(f"\nBúsqueda (Haz) finalizada sin éxito. Nodos expandidos total: {nodos_expandidos}")
        return None