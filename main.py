"""
Script unificado para el proyecto Senku-IA.
Dos modos de uso:
  python main.py --test                      Verificacion completa
  python main.py --algoritmo <alg> --tablero <t> [opciones]  Ejecucion especifica
"""

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.pddl_reader import SenkuPDDLReader
from src.helpers import filtrar_fluentes_relevantes, hash_estado, extraer_adyacencias, contar_piezas
from src.heuristic import funcion_pagoda
from src.basic_search import busqueda_ciega
from src.beam_search import busqueda_haz
from unified_planning.shortcuts import SequentialSimulator

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------
BASE = os.path.dirname(os.path.abspath(__file__))
PDDL_DIR = os.path.join(BASE, "PDDL")
DOMAIN_PATH = os.path.join(PDDL_DIR, "dominio_senku.pddl")

TABLEROS = [
    ("Prueba (3 piezas)",      "problema_senku_prueba.pddl"),
    ("Tablero clasico",        "problema_senku_tablero_clasico.pddl"),
    ("Variante 1",             "problema_senku_tablero_variante1.pddl"),
    ("Variante 3",             "problema_senku_tablero_variante3.pddl"),
    ("Variante 5",             "problema_senku_tablero_variante5.pddl"),
]


# ---------------------------------------------------------------------------
# Colores para consola
# ---------------------------------------------------------------------------
VERDE = "\033[92m"
ROJO = "\033[91m"
AMARILLO = "\033[93m"
AZUL = "\033[94m"
CIAN = "\033[96m"
NEGRITA = "\033[1m"
RESET = "\033[0m"

TICK = f"{VERDE}OK{RESET}"
CROSS = f"{ROJO}XX{RESET}"
ARROW = f"{AZUL}->{RESET}"

def ok(msg):     print(f"  {TICK} {msg}")
def fail(msg):   print(f"  {CROSS} {ROJO}{msg}{RESET}")
def info(msg):   print(f"  {AZUL}i{RESET} {msg}")
def warn(msg):   print(f"  {AMARILLO}!{RESET} {msg}")
def step(msg):   print(f"  {ARROW} {msg}")
def hdr(title):  print(f"\n{NEGRITA}{'='*60}{RESET}\n{NEGRITA}  {title}{RESET}\n{'-'*60}")
def subhdr(title): print(f"\n  {CIAN}--- {title} ---{RESET}")


# ===========================================================================
# Funciones auxiliares de carga
# ===========================================================================

def cargar_todos_los_tableros():
    """
    Carga el dominio y todos los problemas PDDL.
    :return: Diccionario {nombre: (lector, problema)} con las instancias cargadas.
    """
    if not os.path.exists(DOMAIN_PATH):
        fail(f"Archivo de dominio no encontrado: {DOMAIN_PATH}")
        return {}

    ok(f"Dominio: {os.path.basename(DOMAIN_PATH)}")

    instancias = {}
    for nombre, archivo in TABLEROS:
        path = os.path.join(PDDL_DIR, archivo)
        if not os.path.exists(path):
            fail(f"{nombre}: archivo {archivo} no encontrado")
            continue
        try:
            lector = SenkuPDDLReader(DOMAIN_PATH, path)
            problema = lector.read_problem()
            n_objetos = len(list(problema.all_objects))
            n_adyacencias = len(extraer_adyacencias(problema.initial_values))
            instancias[nombre] = (lector, problema)
            ok(f"{nombre}: {n_objetos} casillas, {n_adyacencias} adyacencias")
        except Exception as e:
            fail(f"{nombre}: error al cargar - {e}")

    return instancias


def cargar_tablero(nombre_tablero):
    """
    Carga un unico tablero por su nombre clave.
    :param nombre_tablero: Clave del tablero (ej. 'clasico', 'variante1').
    :return: (lector, problema) o None si no se encuentra.
    """
    mapa = {
        "prueba":     ("Prueba (3 piezas)",      "problema_senku_prueba.pddl"),
        "clasico":    ("Tablero clasico",         "problema_senku_tablero_clasico.pddl"),
        "variante1":  ("Variante 1",              "problema_senku_tablero_variante1.pddl"),
        "variante3":  ("Variante 3",              "problema_senku_tablero_variante3.pddl"),
        "variante5":  ("Variante 5",              "problema_senku_tablero_variante5.pddl"),
    }
    if nombre_tablero not in mapa:
        print(f"Tablero '{nombre_tablero}' no reconocido.")
        print(f"Opciones: {', '.join(mapa.keys())}")
        return None
    nombre, archivo = mapa[nombre_tablero]
    path = os.path.join(PDDL_DIR, archivo)
    if not os.path.exists(path):
        print(f"Archivo no encontrado: {path}")
        return None
    try:
        lector = SenkuPDDLReader(DOMAIN_PATH, path)
        problema = lector.read_problem()
        return lector, problema
    except Exception as e:
        print(f"Error al cargar {nombre}: {e}")
        return None


# ===========================================================================
# Validacion de tableros
# ===========================================================================

def validar_tablero(problema, nombre="", silencioso=False):
    """
    Verifica que el estado inicial del tablero sea consistente:
    - No hay casillas marcadas como pieza y vacio simultaneamente.
    :return: True si es valido, False en caso contrario.
    """
    celdas_con_pieza = set()
    celdas_vacias = set()
    adyacencias = []

    for k, v in problema.initial_values.items():
        name = k.fluent().name
        if name == "pieza" and v.is_true():
            celdas_con_pieza.add(str(k.args[0]))
        elif name == "vacio" and v.is_true():
            celdas_vacias.add(str(k.args[0]))
        elif name == "adyacente" and v.is_true():
            adyacencias.append(tuple(str(a) for a in k.args))

    n_total = len(celdas_con_pieza) + len(celdas_vacias)
    if not silencioso:
        info(f"{nombre}: {n_total} casillas ({len(celdas_con_pieza)} piezas, {len(celdas_vacias)} vacios)")

    duplicadas = celdas_con_pieza & celdas_vacias
    if duplicadas:
        if not silencioso:
            fail(f"Casillas con pieza Y vacio: {duplicadas}")
        return False
    if not silencioso:
        ok("Estado inicial consistente (pieza/vacio mutuamente exclusivos)")
        info(f"Adyacencias: {len(adyacencias)} ({len(adyacencias)//2} unicas bidireccionales)")

    saltos_iniciales = sum(
        1 for o, i, d in adyacencias
        if o in celdas_con_pieza and i in celdas_con_pieza and d in celdas_vacias
    )
    if not silencioso:
        info(f"Movimientos posibles desde inicio: {saltos_iniciales}")

    return True


# ===========================================================================
# Validacion de plan
# ===========================================================================

def validar_plan(problema, plan, nombre="", goal_anywhere=True):
    """
    Ejecuta el plan paso a paso comprobando que cada movimiento es valido
    y que el estado final cumple el objetivo.
    :param goal_anywhere: Si True, acepta cualquier estado con 1 pieza como solucion.
    :return: True si el plan es valido, False en caso contrario.
    """
    from src.helpers import filtrar_fluentes_relevantes
    cached_keys = filtrar_fluentes_relevantes(problema.initial_values)

    with SequentialSimulator(problem=problema) as sim:
        estado = sim.get_initial_state()
        for i, a in enumerate(plan):
            if hasattr(a, 'action'):
                act = a.action
                params = a.actual_parameters
            elif isinstance(a, tuple):
                act = a[0]
                params = a[1]
            else:
                fail(f"Paso {i+1}: formato de accion no reconocido")
                return False

            if not sim.is_applicable(estado, act, params):
                fail(f"Paso {i+1}: movimiento NO valido")
                return False
            estado = sim.apply(estado, act, params)

        if goal_anywhere:
            if contar_piezas(estado, cached_keys) <= 1:
                ok(f"{nombre}: plan validado ({len(plan)} pasos, 1 pieza restante)")
                return True
            else:
                fail(f"{nombre}: el plan no cumple el objetivo ({contar_piezas(estado, cached_keys)} piezas restantes)")
                return False
        else:
            if sim.is_goal(estado):
                ok(f"{nombre}: plan validado ({len(plan)} pasos, estado final = OBJETIVO)")
                return True
            else:
                fail(f"{nombre}: el plan no cumple el objetivo")
                return False


# ===========================================================================
# Impresion del plan
# ===========================================================================

def imprimir_plan(plan, titulo="SOLUCION ENCONTRADA"):
    """
    Muestra la secuencia de acciones de forma legible.
    """
    if plan is None:
        print("  No se encontro solucion.\n")
        return

    if len(plan) == 0:
        print("  El plan esta vacio (el estado inicial ya era la solucion).\n")
        return

    print(f"\n  {NEGRITA}{'='*50}{RESET}")
    print(f"  {NEGRITA}{titulo}{RESET}")
    print(f"  {NEGRITA}{'='*50}{RESET}")

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
            print(f"  Paso {i+1}: {nombre_accion.capitalize()} -> "
                  f"Pieza en {parametros[0]} salta sobre {parametros[1]} hacia {parametros[2]}")
        else:
            print(f"  Paso {i+1}: {nombre_accion.capitalize()} con parametros {parametros}")

    print(f"  {NEGRITA}{'='*50}{RESET}\n")


# ===========================================================================
# Pruebas de verificacion (modo --test)
# ===========================================================================

def test_carga_pddl(instancias):
    """Verifica que todos los archivos PDDL se carguen correctamente."""
    hdr("1. CARGA DE ARCHIVOS PDDL")
    if not instancias:
        fail("No se pudo cargar ningun tablero")
        return False
    ok(f"{len(instancias)}/{len(TABLEROS)} tableros cargados correctamente")
    return True


def test_validacion_tableros(instancias):
    """Verifica la consistencia de cada tablero."""
    hdr("2. VALIDACION DE TABLEROS")
    todo_ok = True
    for nombre in instancias:
        _, problema = instancias[nombre]
        subhdr(nombre)
        if not validar_tablero(problema, nombre):
            todo_ok = False
    return todo_ok


def test_funcion_pagoda(instancias):
    """Verifica las tres variantes de pagoda (V1, V2, V3) en todos los tableros."""
    hdr("3. FUNCION PAGODA (VARIANTES V1/V2/V3)")

    for nombre in instancias:
        lector, _ = instancias[nombre]
        subhdr(nombre)
        try:
            fluentes = lector.cargar_fluentes()
            v1 = funcion_pagoda(fluentes, variante=1)
            v2 = funcion_pagoda(fluentes, variante=2)
            v3 = funcion_pagoda(fluentes, variante=3)
            ok(f"V1={v1}, V2={v2}, V3={v3}")
        except Exception as e:
            fail(f"{nombre}: {e}")

    subhdr("Compatibilidad con strings (formato hash_estado)")
    if "Prueba (3 piezas)" in instancias:
        lector_test, prob_test = instancias["Prueba (3 piezas)"]
        cached_keys = filtrar_fluentes_relevantes(prob_test.initial_values)
        with SequentialSimulator(problem=prob_test) as sim:
            estado = sim.get_initial_state()
            h = hash_estado(estado, cached_keys)
            val_str = funcion_pagoda(h, variante=1)
            fluentes = lector_test.cargar_fluentes()
            val_obj = funcion_pagoda(fluentes, variante=1)
            ok(f"V1: string={val_str}, objeto={val_obj} -- "
               f"{'COINCIDEN' if val_str==val_obj else 'DIFERENTES'}")
    else:
        fail("Tablero de prueba no disponible para test de compatibilidad")

    return True


def test_busqueda_basica(instancias):
    """Verifica BFS y DFS en el tablero de prueba (3 piezas)."""
    hdr("4. BUSQUEDA BASICA - PROBLEMA DE PRUEBA")

    if "Prueba (3 piezas)" not in instancias:
        fail("Problema de prueba no cargado")
        return False

    _, prob_test = instancias["Prueba (3 piezas)"]
    todo_ok = True

    for modo_nombre, bfs_flag in [("BFS (Anchura)", True), ("DFS (Profundidad)", False)]:
        subhdr(modo_nombre)
        t0 = time.time()
        plan = busqueda_ciega(prob_test, usar_bfs=bfs_flag, max_profundidad=10)
        t = time.time() - t0

        if plan is not None:
            ok(f"Solucion encontrada: {len(plan)} pasos en {t:.3f}s")
            for i, a in enumerate(plan):
                if isinstance(a, tuple):
                    params = [str(p) for p in a[1]]
                    step(f"Paso {i+1}: pieza en {params[0]} salta sobre {params[1]} hacia {params[2]}")

            if not validar_plan(prob_test, plan, modo_nombre):
                todo_ok = False
        else:
            fail("No se encontro solucion (inesperado)")
            todo_ok = False

    return todo_ok


def test_beam_search(instancias):
    """Verifica beam search con las configuraciones optimas por tablero."""
    hdr("5. BEAM SEARCH")

    tableros_beam = [k for k in instancias if k != "Prueba (3 piezas)"]
    todo_ok = True
    # (haz, pagoda_primaria, pagoda_secundaria, usar_pagoda_all)
    # pagoda_secundaria: None=auto, 0=sin secundaria, 1/2/3=especifica
    configs = {
        "Tablero clasico":   (500,  1, 0,     False),
        "Variante 1":        (1000, 1, 3,     False),
        "Variante 3":        (1500, 3, 1,     False),
        "Variante 5":        (3000, 1, None,  True),
    }

    for nombre in tableros_beam:
        _, problema = instancias[nombre]
        haz, pagoda, pagoda_sec, pagoda_all = configs.get(nombre, (200, 1, None, False))

        if pagoda_all:
            label = "V1+V2+V3"
        elif pagoda_sec == 0:
            label = f"V{pagoda}"
        elif pagoda_sec is not None:
            label = f"V{pagoda}+V{pagoda_sec}"
        else:
            label = f"V{pagoda}+V{_pagoda_secundaria(pagoda)}"

        subhdr(f"Beam Search - {nombre} (haz={haz}, pagoda={label}, goal_anywhere=True)")

        t0 = time.time()
        if pagoda_all:
            plan = busqueda_haz(problema, tamano_haz=haz, max_profundidad=200,
                                variantes_pagoda=[1, 2, 3], goal_anywhere=True)
        elif pagoda_sec == 0:
            plan = busqueda_haz(problema, tamano_haz=haz, max_profundidad=200,
                                variante_pagoda=pagoda, goal_anywhere=True)
        elif pagoda_sec is not None:
            plan = busqueda_haz(problema, tamano_haz=haz, max_profundidad=200,
                                variante_pagoda=pagoda,
                                variante_pagoda_secundaria=pagoda_sec,
                                goal_anywhere=True)
        else:
            plan = busqueda_haz(problema, tamano_haz=haz, max_profundidad=200,
                                variante_pagoda=pagoda,
                                variante_pagoda_secundaria=_pagoda_secundaria(pagoda),
                                goal_anywhere=True)
        t = time.time() - t0

        if plan is not None:
            ok(f"Solucion encontrada ({label}): {len(plan)} pasos en {t:.3f}s")
            imprimir_plan(plan, f"Plan - {nombre}")
            if not validar_plan(problema, plan, nombre, goal_anywhere=True):
                todo_ok = False
        else:
            warn(f"No se encontro solucion para {nombre} con haz={haz}, pagoda={label} tras {t:.1f}s")

    return todo_ok


def ejecutar_test_completo():
    """
    Ejecuta todas las verificaciones en orden y muestra un resumen final.
    """
    print(f"\n{NEGRITA}{'='*60}{RESET}")
    print(f"{NEGRITA}  VERIFICACION COMPLETA - SENKU IA{RESET}")
    print(f"{NEGRITA}{'='*60}{RESET}\n")

    resultados = []

    instancias = cargar_todos_los_tableros()
    resultados.append(("Carga PDDL", test_carga_pddl(instancias)))

    if not instancias:
        print(f"\n{NEGRITA}No hay tableros cargados. Abortando.{RESET}\n")
        return

    resultados.append(("Validacion tableros", test_validacion_tableros(instancias)))
    resultados.append(("Funcion pagoda", test_funcion_pagoda(instancias)))
    resultados.append(("Busqueda basica", test_busqueda_basica(instancias)))
    resultados.append(("Beam Search", test_beam_search(instancias)))

    # Resumen final
    hdr("RESUMEN FINAL")
    todos_ok = True
    for nombre, resultado in resultados:
        if resultado:
            ok(f"{nombre}: COMPLETADO")
        else:
            fail(f"{nombre}: FALLOS DETECTADOS")
            todos_ok = False

    if todos_ok:
        print(f"\n  {NEGRITA}{VERDE}¡Todas las verificaciones superadas!{RESET}{NEGRITA}{RESET}\n")
    else:
        print(f"\n  {NEGRITA}{ROJO}Algunas verificaciones fallaron. Revise los detalles arriba.{RESET}{NEGRITA}{RESET}\n")


# ===========================================================================
# Ejecucion especifica (modo --algoritmo)
# ===========================================================================

def ejecutar_basica(problema, usar_bfs, max_profundidad=None):
    """Ejecuta busqueda basica (BFS/DFS) y muestra el resultado."""
    modo = "BFS" if usar_bfs else "DFS"
    print(f"{NEGRITA}Busqueda basica ({modo}){RESET}")
    print(f"{'='*40}")

    t0 = time.time()
    plan = busqueda_ciega(problema, usar_bfs=usar_bfs, max_profundidad=max_profundidad)
    t = time.time() - t0

    if plan is not None:
        pasos = len(plan)
        print(f"\nSolucion encontrada: {pasos} pasos en {t:.3f}s")
        imprimir_plan(plan)
        valida = validar_plan(problema, plan, "Plan")
        print(f"Plan valido: {TICK if valida else CROSS}")
    else:
        print(f"\nNo se encontro solucion tras {t:.3f}s")

    print(f"Tiempo total: {t:.4f}s\n")


def _pagoda_secundaria(v, override=None):
    return override if override is not None else {1: 2, 2: 3, 3: 1}.get(v)

def ejecutar_beam(problema, tamano_haz, max_profundidad, variante_pagoda, variante_pagoda_secundaria=None, goal_anywhere=True, pagoda_all=False):
    """Ejecuta beam search con pagoda y muestra el resultado."""
    t0 = time.time()

    if pagoda_all:
        print(f"{NEGRITA}Beam Search (haz={tamano_haz}, profundidad={max_profundidad or 'sin limite'}, "
              f"pagoda=V1+V2+V3, goal_anywhere={goal_anywhere}){RESET}")
        print(f"{'='*60}")
        plan = busqueda_haz(problema, tamano_haz=tamano_haz,
                            max_profundidad=max_profundidad,
                            variantes_pagoda=[1, 2, 3],
                            goal_anywhere=goal_anywhere)
    else:
        v_sec = _pagoda_secundaria(variante_pagoda, variante_pagoda_secundaria)
        print(f"{NEGRITA}Beam Search (haz={tamano_haz}, profundidad={max_profundidad or 'sin limite'}, "
              f"pagoda=V{variante_pagoda}+V{v_sec}, goal_anywhere={goal_anywhere}){RESET}")
        print(f"{'='*60}")
        plan = busqueda_haz(problema, tamano_haz=tamano_haz,
                            max_profundidad=max_profundidad,
                            variante_pagoda=variante_pagoda,
                            variante_pagoda_secundaria=v_sec,
                            goal_anywhere=goal_anywhere)
    t = time.time() - t0

    if plan is not None:
        pasos = len(plan)
        print(f"\nSolucion encontrada: {pasos} pasos en {t:.3f}s")
        imprimir_plan(plan)
        valida = validar_plan(problema, plan, "Plan", goal_anywhere=goal_anywhere)
        print(f"Plan valido: {TICK if valida else CROSS}")
    else:
        print(f"\nNo se encontro solucion tras {t:.3f}s")

    print(f"Tiempo total: {t:.4f}s\n")


# ===========================================================================
# Parseo de argumentos
# ===========================================================================

def parse_args():
    parser = argparse.ArgumentParser(
        description="Senku-IA: planificacion automatica aplicada al Senku",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Ejemplos de uso:
  {os.path.basename(__file__)} --test
  {os.path.basename(__file__)} --algoritmo beam --tablero clasico --haz 200
  {os.path.basename(__file__)} --algoritmo basic --dfs --tablero variante1
  {os.path.basename(__file__)} --algoritmo beam --tablero variante5 --haz 100 --pagoda 2
  # Las variantes de pagoda son: 1 (V1), 2 (V2), 3 (V3).
  # Pagoda secundaria por defecto: 1->2, 2->3, 3->1. Usar --pagoda-sec para override.
  # --pagoda-all usa las tres variantes como clave de ordenacion (V1+V2+V3), ideal para V5.
  # Ej: --pagoda 2 --pagoda-sec 1  -> primaria V2, secundaria V1.
        """
    )

    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--test", action="store_true",
                       help="Ejecuta la bateria completa de verificacion")
    grupo.add_argument("--algoritmo", type=str, choices=["basic", "beam"],
                       help="Algoritmo a ejecutar (basic o beam)")

    parser.add_argument("--tablero", type=str, default="clasico",
                        choices=["prueba", "clasico", "variante1", "variante3", "variante5"],
                        help="Tablero a resolver (defecto: clasico)")

    parser.add_argument("--bfs", action="store_true",
                        help="[basic] Usar busqueda en anchura (BFS)")
    parser.add_argument("--dfs", action="store_true",
                        help="[basic] Usar busqueda en profundidad (DFS)")

    parser.add_argument("--haz", type=int, default=50,
                        help="[beam] Anchura del haz (defecto: 50)")
    parser.add_argument("--pagoda", type=int, default=1, choices=[1, 2, 3],
                        help="[beam] Variante de pagoda primaria (1, 2 o 3, defecto: 1)")
    parser.add_argument("--pagoda-sec", type=int, default=None, choices=[1, 2, 3],
                        help="[beam] Variante de pagoda secundaria (defecto: auto 1->2, 2->3, 3->1)")
    parser.add_argument("--pagoda-all", action="store_true",
                        help="[beam] Usa las tres variantes de pagoda (V1+V2+V3) como clave de ordenacion")

    parser.add_argument("--max-profundidad", type=int, default=None,
                        help="Limite de profundidad (defecto: sin limite)")
    parser.add_argument("--goal-especifico", action="store_true",
                        help="Usa el objetivo exacto del PDDL (por defecto: cualquier pieza unica vale)")

    return parser.parse_args()


# ===========================================================================
# Punto de entrada
# ===========================================================================

def main():
    args = parse_args()

    if args.test:
        ejecutar_test_completo()
        return

    # Modo algoritmo especifico
    if args.algoritmo == "basic":
        usar_bfs = True
        if args.dfs and not args.bfs:
            usar_bfs = False

        resultado = cargar_tablero(args.tablero)
        if resultado is None:
            sys.exit(1)
        _, problema = resultado
        ejecutar_basica(problema, usar_bfs, args.max_profundidad)

    elif args.algoritmo == "beam":
        resultado = cargar_tablero(args.tablero)
        if resultado is None:
            sys.exit(1)
        _, problema = resultado
        ejecutar_beam(problema, args.haz, args.max_profundidad, args.pagoda,
                      variante_pagoda_secundaria=args.pagoda_sec,
                      goal_anywhere=not args.goal_especifico,
                      pagoda_all=args.pagoda_all)


if __name__ == "__main__":
    main()
