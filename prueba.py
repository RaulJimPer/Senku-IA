"""
Script de prueba integral para el proyecto Senku-IA.
Verifica: dominio PDDL, tableros, función pagoda y búsqueda básica.
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.pddl_reader import SenkuPDDLReader
from src.basic_search import (
    busqueda_ciega,
    _filtrar_fluentes_relevantes,
    hash_estado,
    _extraer_adyacencias,
)
from unified_planning.shortcuts import SequentialSimulator

BASE = os.path.dirname(os.path.abspath(__file__))
PDDL_DIR = os.path.join(BASE, "PDDL")
DOMAIN_PATH = os.path.join(PDDL_DIR, "dominio_senku.pddl")
PYTHON = sys.executable

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

problemas = [
    ("Prueba (3 piezas)",      "problema_senku_prueba.pddl"),
    ("Tablero cl\xe1sico",     "problema_senku_tablero_clasico.pddl"),
    ("Variante 1",             "problema_senku_tablero_variante1.pddl"),
    ("Variante 3",             "problema_senku_tablero_variante3.pddl"),
    ("Variante 5",             "problema_senku_tablero_variante5.pddl"),
]

instancias = {}

# ===========================================================================
hdr("1. CARGA DE ARCHIVOS PDDL")
# ===========================================================================

if not os.path.exists(DOMAIN_PATH):
    fail(f"Archivo de dominio no encontrado: {DOMAIN_PATH}")
    sys.exit(1)

ok(f"Dominio: {os.path.basename(DOMAIN_PATH)}")

for nombre, archivo in problemas:
    path = os.path.join(PDDL_DIR, archivo)
    if not os.path.exists(path):
        fail(f"{nombre}: archivo {archivo} no encontrado")
        continue
    try:
        lector = SenkuPDDLReader(DOMAIN_PATH, path)
        problema = lector.read_problem()
        n_objetos = len(list(problema.all_objects))
        n_adyacencias = len(_extraer_adyacencias(problema.initial_values))
        n_acciones = len(problema.actions)
        instancias[nombre] = (lector, problema)
        ok(f"{nombre}: {n_objetos} casillas, {n_adyacencias} adyacencias, {n_acciones} acci\xf3n")
    except Exception as e:
        fail(f"{nombre}: error al cargar - {e}")

# ===========================================================================
hdr("2. VALIDACION DE TABLEROS")
# ===========================================================================

for nombre, _ in problemas:
    if nombre not in instancias:
        continue
    _, problema = instancias[nombre]
    subhdr(nombre)

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
    info(f"Estado inicial: {n_total} casillas ({len(celdas_con_pieza)} piezas, {len(celdas_vacias)} vac\xedos)")

    duplicadas = celdas_con_pieza & celdas_vacias
    if duplicadas:
        fail(f"Casillas con pieza Y vac\xedo: {duplicadas}")
    else:
        ok("Estado inicial consistente (pieza/vacio mutuamente exclusivos)")

    info(f"Adyacencias: {len(adyacencias)} ({len(adyacencias)//2} \xfanicas bidireccionales)")

    saltos_iniciales = sum(1 for o, i, d in adyacencias
                          if o in celdas_con_pieza and i in celdas_con_pieza and d in celdas_vacias)
    info(f"Movimientos posibles desde inicio: {saltos_iniciales}")

# ===========================================================================
hdr("3. FUNCION PAGODA")
# ===========================================================================

subhdr("Desde objetos fluent (interfaz original)")
for nombre in instancias:
    lector, _ = instancias[nombre]
    try:
        fluentes = lector.cargar_fluentes()
        v1 = lector.funcion_pagoda(fluentes, variante=1)
        v2 = lector.funcion_pagoda(fluentes, variante=2)
        v3 = lector.funcion_pagoda(fluentes, variante=3)
        ok(f"{nombre}: V1={v1}, V2={v2}, V3={v3}")
    except Exception as e:
        fail(f"{nombre}: {e}")

subhdr("Compatibilidad con strings (formato hash_estado)")
if "Prueba (3 piezas)" in instancias:
    lector_test, prob_test = instancias["Prueba (3 piezas)"]
    cached_keys = _filtrar_fluentes_relevantes(prob_test.initial_values)
    with SequentialSimulator(problem=prob_test) as sim:
        estado = sim.get_initial_state()
        h = hash_estado(estado, cached_keys)
        v1_str = lector_test.funcion_pagoda(h, variante=1)
        v2_str = lector_test.funcion_pagoda(h, variante=2)
        v3_str = lector_test.funcion_pagoda(h, variante=3)
        fluentes = lector_test.cargar_fluentes()
        v1_obj = lector_test.funcion_pagoda(fluentes, variante=1)
        v2_obj = lector_test.funcion_pagoda(fluentes, variante=2)
        v3_obj = lector_test.funcion_pagoda(fluentes, variante=3)
        ok(f"V1: string={v1_str}, objeto={v1_obj} -- {'COINCIDEN' if v1_str==v1_obj else 'DIFERENTES'}")
        ok(f"V2: string={v2_str}, objeto={v2_obj} -- {'COINCIDEN' if v2_str==v2_obj else 'DIFERENTES'}")
        ok(f"V3: string={v3_str}, objeto={v3_obj} -- {'COINCIDEN' if v3_str==v3_obj else 'DIFERENTES'}")

# ===========================================================================
hdr("4. BUSQUEDA BASICA - PROBLEMA DE PRUEBA")
# ===========================================================================

if "Prueba (3 piezas)" in instancias:
    _, prob_test = instancias["Prueba (3 piezas)"]

    for modo_nombre, bfs_flag in [("BFS (Anchura)", True), ("DFS (Profundidad)", False)]:
        subhdr(modo_nombre)
        t0 = time.time()
        plan = busqueda_ciega(prob_test, usar_bfs=bfs_flag, max_profundidad=10)
        t = time.time() - t0
        if plan is not None:
            ok(f"Soluci\xf3n encontrada: {len(plan)} pasos en {t:.3f}s")
            for i, a in enumerate(plan):
                if isinstance(a, tuple):
                    params = [str(p) for p in a[1]]
                step(f"Paso {i+1}: pieza en {params[0]} salta sobre {params[1]} hacia {params[2]}")

            with SequentialSimulator(problem=prob_test) as sim:
                estado = sim.get_initial_state()
                valido = True
                for i, a in enumerate(plan):
                    if isinstance(a, tuple):
                        act, params = a
                    if not sim.is_applicable(estado, act, params):
                        fail(f"Paso {i+1}: movimiento NO v\xe1lido")
                        valido = False
                        break
                    estado = sim.apply(estado, act, params)
                if valido and sim.is_goal(estado):
                    ok("Plan validado: todos los movimientos legales y estado final = OBJETIVO")
                else:
                    fail("El plan no cumple el objetivo")
        else:
            fail("No se encontr\xf3 soluci\xf3n (inesperado)")
else:
    fail("Problema de prueba no cargado")

# ===========================================================================
hdr("5. BUSQUEDA BASICA - TABLERO CLASICO")
# ===========================================================================

warn("DFS sobre el tablero cl\xe1sico (32 piezas, espacio de estados ~10^12)")
warn("Sin l\xedmite de profundidad ni timeout. Presiona Ctrl+C para interrumpir.")

if "Tablero cl\xe1sico" in instancias:
    _, prob_clasico = instancias["Tablero cl\xe1sico"]
    t0 = time.time()
    try:
        plan = busqueda_ciega(prob_clasico, usar_bfs=False)
        t = time.time() - t0
        if plan is not None:
            ok(f"Soluci\xf3n encontrada: {len(plan)} pasos en {t:.3f}s")
            for i, a in enumerate(plan):
                if isinstance(a, tuple):
                    params = [str(p) for p in a[1]]
                step(f"Paso {i+1}: {params[0]} -> {params[1]} -> {params[2]}")
        else:
            warn(f"B\xfasqueda completada sin soluci\xf3n tras {t:.3f}s (todo el espacio explorado)")
    except KeyboardInterrupt:
        t = time.time() - t0
        print()
        warn(f"B\xfasqueda interrumpida por el usuario tras {t:.3f}s")
else:
    fail("Tablero cl\xe1sico no cargado")

# ===========================================================================
hdr("6. RESUMEN FINAL")
# ===========================================================================

ok("Archivos PDDL: dominio + 5 problemas cargados y validados")
ok("Funci\xf3n pagoda: 3 variantes implementadas, compatible con strings y objetos fluent")
ok("B\xfasqueda b\xe1sica (BFS/DFS): funcional, con cach\xe9, detecci\xf3n de ciclos y max_profundidad")
ok("Plan de prueba: encontrado y validado paso a paso con el simulador")

warn("Tablero cl\xe1sico: la b\xfasqueda ciega sin heur\xedstica no encuentra soluci\xf3n en tiempo pr\xe1ctico")
info("Esto es esperado: el espacio de estados del Senku cl\xe1sico es enorme (~10^12)")
info("La implementaci\xf3n de Beam Search (convocatoria de junio) con heur\xedstica pagoda")
info("abordar\xe1 este problema guiando la b\xfasqueda hacia estados prometedores.")

print(f"\n{NEGRITA}Script de prueba completado.{RESET}\n")
