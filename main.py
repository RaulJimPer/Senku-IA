import os
import time
from src.pddl_reader import SenkuPDDLReader
from src.basic_search import busqueda_ciega
from src.bean_search import busqueda_haz

def imprimir_plan(plan):
    """
    Formatea la lista de acciones devuelta por el algoritmo 
    para que sea legible en la consola.
    """
    if not plan:
        print("El plan está vacío (el estado inicial ya era la solución).")
        return

    print("\n" + "="*40)
    print("SOLUCIÓN ENCONTRADA")
    print("="*40)
    
    for i, accion in enumerate(plan):
        if hasattr(accion, 'action'):
            nombre_accion = accion.action.name
            parametros = [str(p) for p in accion.actual_parameters]
        elif isinstance(accion, tuple):
            nombre_accion = accion[0].name
            parametros = [str(p) for p in accion[1]]
        else:
            nombre_accion = "Accion"
            parametros = ["?", "?", "?"]
        
        if len(parametros) >= 3:
            print(f"Paso {i + 1}: {nombre_accion.capitalize()} -> Pieza en {parametros[0]} salta sobre {parametros[1]} hacia {parametros[2]}")
        else:
            print(f"Paso {i + 1}: {nombre_accion.capitalize()} con parámetros {parametros}")
    
    print("="*40 + "\n")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    domain_path = os.path.join(base_dir, "PDDL", "dominio_senku.pddl")
    problem_path = os.path.join(base_dir, "PDDL", "problema_senku_tablero_clasico.pddl")

    print(f"Cargando dominio desde: {domain_path}")
    print(f"Cargando problema desde: {problem_path}")

    try:
        lector = SenkuPDDLReader(domain_path, problem_path)
        problema = lector.read_problem()
        print("Problema instanciado correctamente.\n")
    except Exception as e:
        print(f"Error al leer los archivos PDDL: {e}")
        exit(1)

    usar_beam_search = True
    usar_anchura = False

    if usar_beam_search:
        modo = "Haz (Beam Search)"
    else:
        modo = "Anchura (BFS)" if usar_anchura else "Profundidad (DFS)"
        
    print(f"Iniciando Búsqueda en {modo}...")
    
    inicio_tiempo = time.time()
    if usar_beam_search:
        plan_solucion = busqueda_haz(problema, tamano_haz=50)
    else:
        plan_solucion = busqueda_ciega(problema, usar_bfs=usar_anchura)
    
    fin_tiempo = time.time()
    tiempo_total = fin_tiempo - inicio_tiempo

    if plan_solucion is not None:
        imprimir_plan(plan_solucion)
        print(f"Tiempo de ejecución: {tiempo_total:.4f} segundos.")
    else:
        print("No se pudo encontrar una solución para este tablero.")
        print(f"Tiempo de ejecución antes de rendirse: {tiempo_total:.4f} segundos.")