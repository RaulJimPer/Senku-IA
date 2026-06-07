```
============================================================
  VERIFICACION COMPLETA - SENKU IA
============================================================

  OK Dominio: dominio_senku.pddl
  OK Prueba (3 piezas): 33 casillas, 76 adyacencias
  OK Tablero clasico: 33 casillas, 76 adyacencias
  OK Variante 1: 37 casillas, 92 adyacencias
  OK Variante 3: 39 casillas, 92 adyacencias
  OK Variante 5: 41 casillas, 100 adyacencias

============================================================
  1. CARGA DE ARCHIVOS PDDL
------------------------------------------------------------
  OK 5/5 tableros cargados correctamente

============================================================
  2. VALIDACION DE TABLEROS
------------------------------------------------------------

  --- Prueba (3 piezas) ---
  i Prueba (3 piezas): 33 casillas (3 piezas, 30 vacios)
  OK Estado inicial consistente (pieza/vacio mutuamente exclusivos)
  i Adyacencias: 76 (38 unicas bidireccionales)
  i Movimientos posibles desde inicio: 2

  --- Tablero clasico ---
  i Tablero clasico: 33 casillas (32 piezas, 1 vacios)
  OK Estado inicial consistente (pieza/vacio mutuamente exclusivos)
  i Adyacencias: 76 (38 unicas bidireccionales)
  i Movimientos posibles desde inicio: 4

  --- Variante 1 ---
  i Variante 1: 37 casillas (36 piezas, 1 vacios)
  OK Estado inicial consistente (pieza/vacio mutuamente exclusivos)
  i Adyacencias: 92 (46 unicas bidireccionales)
  i Movimientos posibles desde inicio: 4

  --- Variante 3 ---
  i Variante 3: 39 casillas (38 piezas, 1 vacios)
  OK Estado inicial consistente (pieza/vacio mutuamente exclusivos)
  i Adyacencias: 92 (46 unicas bidireccionales)
  i Movimientos posibles desde inicio: 4

  --- Variante 5 ---
  i Variante 5: 41 casillas (40 piezas, 1 vacios)
  OK Estado inicial consistente (pieza/vacio mutuamente exclusivos)
  i Adyacencias: 100 (50 unicas bidireccionales)
  i Movimientos posibles desde inicio: 4

============================================================
  3. FUNCION PAGODA (VARIANTES V1/V2/V3)
------------------------------------------------------------

  --- Prueba (3 piezas) ---
  OK V1=1, V2=1, V3=1

  --- Tablero clasico ---
  OK V1=12, V2=4, V3=8

  --- Variante 1 ---
  OK V1=12, V2=9, V3=7

  --- Variante 3 ---
  OK V1=12, V2=6, V3=10

  --- Variante 5 ---
  OK V1=12, V2=12, V3=8

  --- Compatibilidad con strings (formato hash_estado) ---
  OK V1: string=1, objeto=1 -- COINCIDEN

============================================================
  4. BUSQUEDA BASICA - PROBLEMA DE PRUEBA
------------------------------------------------------------

  --- BFS (Anchura) ---

Solucion encontrada! Nodos expandidos: 3
Profundidad de la solucion (saltos): 2
  OK Solucion encontrada: 2 pasos en 0.871s
  -> Paso 1: pieza en c25 salta sobre c35 hacia c45
  -> Paso 2: pieza en c46 salta sobre c45 hacia c44
  OK BFS (Anchura): plan validado (2 pasos, 1 pieza restante)

  --- DFS (Profundidad) ---

Solucion encontrada! Nodos expandidos: 2
Profundidad de la solucion (saltos): 2
  OK Solucion encontrada: 2 pasos en 0.880s
  -> Paso 1: pieza en c25 salta sobre c35 hacia c45
  -> Paso 2: pieza en c46 salta sobre c45 hacia c44
  OK DFS (Profundidad): plan validado (2 pasos, 1 pieza restante)

============================================================
  5. BEAM SEARCH
------------------------------------------------------------

  --- Beam Search - Tablero clasico (haz=500, pagoda=V1, goal_anywhere=True) ---
Nivel: 0, Nodos en este nivel: 1, Nodos expandidos hasta ahora: 0
Nivel: 1, Nodos en este nivel: 4, Nodos expandidos hasta ahora: 1
Nivel: 2, Nodos en este nivel: 12, Nodos expandidos hasta ahora: 5
Nivel: 3, Nodos en este nivel: 60, Nodos expandidos hasta ahora: 17
Nivel: 4, Nodos en este nivel: 296, Nodos expandidos hasta ahora: 77
Nivel: 5, Nodos en este nivel: 500, Nodos expandidos hasta ahora: 373
Nivel: 6, Nodos en este nivel: 500, Nodos expandidos hasta ahora: 873
Nivel: 7, Nodos en este nivel: 500, Nodos expandidos hasta ahora: 1373
Nivel: 8, Nodos en este nivel: 500, Nodos expandidos hasta ahora: 1873
Nivel: 9, Nodos en este nivel: 500, Nodos expandidos hasta ahora: 2373
Nivel: 10, Nodos en este nivel: 500, Nodos expandidos hasta ahora: 2873
Nivel: 11, Nodos en este nivel: 500, Nodos expandidos hasta ahora: 3373
Nivel: 12, Nodos en este nivel: 500, Nodos expandidos hasta ahora: 3873
Nivel: 13, Nodos en este nivel: 500, Nodos expandidos hasta ahora: 4373
Nivel: 14, Nodos en este nivel: 500, Nodos expandidos hasta ahora: 4873
Nivel: 15, Nodos en este nivel: 500, Nodos expandidos hasta ahora: 5373
Nivel: 16, Nodos en este nivel: 500, Nodos expandidos hasta ahora: 5873
Nivel: 17, Nodos en este nivel: 500, Nodos expandidos hasta ahora: 6373
Nivel: 18, Nodos en este nivel: 500, Nodos expandidos hasta ahora: 6873
Nivel: 19, Nodos en este nivel: 500, Nodos expandidos hasta ahora: 7373
Nivel: 20, Nodos en este nivel: 500, Nodos expandidos hasta ahora: 7873
Nivel: 21, Nodos en este nivel: 500, Nodos expandidos hasta ahora: 8373
Nivel: 22, Nodos en este nivel: 500, Nodos expandidos hasta ahora: 8873
Nivel: 23, Nodos en este nivel: 500, Nodos expandidos hasta ahora: 9373
Nivel: 24, Nodos en este nivel: 500, Nodos expandidos hasta ahora: 9873
Nivel: 25, Nodos en este nivel: 500, Nodos expandidos hasta ahora: 10373
Nivel: 26, Nodos en este nivel: 408, Nodos expandidos hasta ahora: 10873
Nivel: 27, Nodos en este nivel: 232, Nodos expandidos hasta ahora: 11281
Nivel: 28, Nodos en este nivel: 97, Nodos expandidos hasta ahora: 11513
Nivel: 29, Nodos en este nivel: 55, Nodos expandidos hasta ahora: 11610
Nivel: 30, Nodos en este nivel: 7, Nodos expandidos hasta ahora: 11665

Solucion encontrada con Beam Search! Nodos expandidos total: 11667
Profundidad de la solucion (saltos): 31
  OK Solucion encontrada (V1): 31 pasos en 43.748s

  ==================================================
  Plan - Tablero clasico
  ==================================================
  Paso 1: Saltar -> Pieza en c24 salta sobre c34 hacia c44
  Paso 2: Saltar -> Pieza en c32 salta sobre c33 hacia c34
  Paso 3: Saltar -> Pieza en c13 salta sobre c23 hacia c33
  Paso 4: Saltar -> Pieza en c34 salta sobre c33 hacia c32
  Paso 5: Saltar -> Pieza en c36 salta sobre c35 hacia c34
  Paso 6: Saltar -> Pieza en c31 salta sobre c32 hacia c33
  Paso 7: Saltar -> Pieza en c43 salta sobre c33 hacia c23
  Paso 8: Saltar -> Pieza en c63 salta sobre c53 hacia c43
  Paso 9: Saltar -> Pieza en c51 salta sobre c52 hacia c53
  Paso 10: Saltar -> Pieza en c54 salta sobre c53 hacia c52
  Paso 11: Saltar -> Pieza en c56 salta sobre c55 hacia c54
  Paso 12: Saltar -> Pieza en c15 salta sobre c25 hacia c35
  Paso 13: Saltar -> Pieza en c34 salta sobre c35 hacia c36
  Paso 14: Saltar -> Pieza en c75 salta sobre c65 hacia c55
  Paso 15: Saltar -> Pieza en c54 salta sobre c55 hacia c56
  Paso 16: Saltar -> Pieza en c37 salta sobre c36 hacia c35
  Paso 17: Saltar -> Pieza en c45 salta sobre c35 hacia c25
  Paso 18: Saltar -> Pieza en c43 salta sobre c44 hacia c45
  Paso 19: Saltar -> Pieza en c57 salta sobre c56 hacia c55
  Paso 20: Saltar -> Pieza en c45 salta sobre c55 hacia c65
  Paso 21: Saltar -> Pieza en c41 salta sobre c42 hacia c43
  Paso 22: Saltar -> Pieza en c47 salta sobre c46 hacia c45
  Paso 23: Saltar -> Pieza en c73 salta sobre c74 hacia c75
  Paso 24: Saltar -> Pieza en c75 salta sobre c65 hacia c55
  Paso 25: Saltar -> Pieza en c55 salta sobre c45 hacia c35
  Paso 26: Saltar -> Pieza en c35 salta sobre c25 hacia c15
  Paso 27: Saltar -> Pieza en c15 salta sobre c14 hacia c13
  Paso 28: Saltar -> Pieza en c13 salta sobre c23 hacia c33
  Paso 29: Saltar -> Pieza en c33 salta sobre c43 hacia c53
  Paso 30: Saltar -> Pieza en c52 salta sobre c53 hacia c54
  Paso 31: Saltar -> Pieza en c64 salta sobre c54 hacia c44
  ==================================================

  OK Tablero clasico: plan validado (31 pasos, 1 pieza restante)

  --- Beam Search - Variante 1 (haz=1000, pagoda=V1+V3, goal_anywhere=True) ---
Nivel: 0, Nodos en este nivel: 1, Nodos expandidos hasta ahora: 0
Nivel: 1, Nodos en este nivel: 4, Nodos expandidos hasta ahora: 1
Nivel: 2, Nodos en este nivel: 17, Nodos expandidos hasta ahora: 5
Nivel: 3, Nodos en este nivel: 92, Nodos expandidos hasta ahora: 22
Nivel: 4, Nodos en este nivel: 495, Nodos expandidos hasta ahora: 114
Nivel: 5, Nodos en este nivel: 1000, Nodos expandidos hasta ahora: 609
Nivel: 6, Nodos en este nivel: 1000, Nodos expandidos hasta ahora: 1609
Nivel: 7, Nodos en este nivel: 1000, Nodos expandidos hasta ahora: 2609
Nivel: 8, Nodos en este nivel: 1000, Nodos expandidos hasta ahora: 3609
Nivel: 9, Nodos en este nivel: 1000, Nodos expandidos hasta ahora: 4609
Nivel: 10, Nodos en este nivel: 1000, Nodos expandidos hasta ahora: 5609
Nivel: 11, Nodos en este nivel: 1000, Nodos expandidos hasta ahora: 6609
Nivel: 12, Nodos en este nivel: 1000, Nodos expandidos hasta ahora: 7609
Nivel: 13, Nodos en este nivel: 1000, Nodos expandidos hasta ahora: 8609
Nivel: 14, Nodos en este nivel: 1000, Nodos expandidos hasta ahora: 9609
Nivel: 15, Nodos en este nivel: 1000, Nodos expandidos hasta ahora: 10609
Nivel: 16, Nodos en este nivel: 1000, Nodos expandidos hasta ahora: 11609
Nivel: 17, Nodos en este nivel: 1000, Nodos expandidos hasta ahora: 12609
Nivel: 18, Nodos en este nivel: 1000, Nodos expandidos hasta ahora: 13609
Nivel: 19, Nodos en este nivel: 1000, Nodos expandidos hasta ahora: 14609
Nivel: 20, Nodos en este nivel: 1000, Nodos expandidos hasta ahora: 15609
Nivel: 21, Nodos en este nivel: 1000, Nodos expandidos hasta ahora: 16609
Nivel: 22, Nodos en este nivel: 1000, Nodos expandidos hasta ahora: 17609
Nivel: 23, Nodos en este nivel: 1000, Nodos expandidos hasta ahora: 18609
Nivel: 24, Nodos en este nivel: 1000, Nodos expandidos hasta ahora: 19609
Nivel: 25, Nodos en este nivel: 1000, Nodos expandidos hasta ahora: 20609
Nivel: 26, Nodos en este nivel: 1000, Nodos expandidos hasta ahora: 21609
Nivel: 27, Nodos en este nivel: 1000, Nodos expandidos hasta ahora: 22609
Nivel: 28, Nodos en este nivel: 1000, Nodos expandidos hasta ahora: 23609
Nivel: 29, Nodos en este nivel: 906, Nodos expandidos hasta ahora: 24609
Nivel: 30, Nodos en este nivel: 646, Nodos expandidos hasta ahora: 25515
Nivel: 31, Nodos en este nivel: 384, Nodos expandidos hasta ahora: 26161
Nivel: 32, Nodos en este nivel: 163, Nodos expandidos hasta ahora: 26545
Nivel: 33, Nodos en este nivel: 50, Nodos expandidos hasta ahora: 26708
Nivel: 34, Nodos en este nivel: 11, Nodos expandidos hasta ahora: 26758

Solucion encontrada con Beam Search! Nodos expandidos total: 26763
Profundidad de la solucion (saltos): 35
  OK Solucion encontrada (V1+V3): 35 pasos en 138.335s

  ==================================================
  Plan - Variante 1
  ==================================================
  Paso 1: Saltar -> Pieza en c23 salta sobre c33 hacia c43
  Paso 2: Saltar -> Pieza en c31 salta sobre c32 hacia c33
  Paso 3: Saltar -> Pieza en c43 salta sobre c33 hacia c23
  Paso 4: Saltar -> Pieza en c63 salta sobre c53 hacia c43
  Paso 5: Saltar -> Pieza en c13 salta sobre c23 hacia c33
  Paso 6: Saltar -> Pieza en c34 salta sobre c33 hacia c32
  Paso 7: Saltar -> Pieza en c36 salta sobre c35 hacia c34
  Paso 8: Saltar -> Pieza en c51 salta sobre c52 hacia c53
  Paso 9: Saltar -> Pieza en c43 salta sobre c53 hacia c63
  Paso 10: Saltar -> Pieza en c73 salta sobre c63 hacia c53
  Paso 11: Saltar -> Pieza en c54 salta sobre c53 hacia c52
  Paso 12: Saltar -> Pieza en c56 salta sobre c55 hacia c54
  Paso 13: Saltar -> Pieza en c15 salta sobre c25 hacia c35
  Paso 14: Saltar -> Pieza en c34 salta sobre c35 hacia c36
  Paso 15: Saltar -> Pieza en c75 salta sobre c65 hacia c55
  Paso 16: Saltar -> Pieza en c54 salta sobre c55 hacia c56
  Paso 17: Saltar -> Pieza en c37 salta sobre c36 hacia c35
  Paso 18: Saltar -> Pieza en c45 salta sobre c35 hacia c25
  Paso 19: Saltar -> Pieza en c47 salta sobre c46 hacia c45
  Paso 20: Saltar -> Pieza en c57 salta sobre c56 hacia c55
  Paso 21: Saltar -> Pieza en c45 salta sobre c55 hacia c65
  Paso 22: Saltar -> Pieza en c14 salta sobre c24 hacia c34
  Paso 23: Saltar -> Pieza en c26 salta sobre c25 hacia c24
  Paso 24: Saltar -> Pieza en c74 salta sobre c64 hacia c54
  Paso 25: Saltar -> Pieza en c66 salta sobre c65 hacia c64
  Paso 26: Saltar -> Pieza en c41 salta sobre c42 hacia c43
  Paso 27: Saltar -> Pieza en c22 salta sobre c32 hacia c42
  Paso 28: Saltar -> Pieza en c52 salta sobre c42 hacia c32
  Paso 29: Saltar -> Pieza en c43 salta sobre c44 hacia c45
  Paso 30: Saltar -> Pieza en c24 salta sobre c34 hacia c44
  Paso 31: Saltar -> Pieza en c45 salta sobre c44 hacia c43
  Paso 32: Saltar -> Pieza en c64 salta sobre c54 hacia c44
  Paso 33: Saltar -> Pieza en c44 salta sobre c43 hacia c42
  Paso 34: Saltar -> Pieza en c32 salta sobre c42 hacia c52
  Paso 35: Saltar -> Pieza en c62 salta sobre c52 hacia c42
  ==================================================

  OK Variante 1: plan validado (35 pasos, 1 pieza restante)

  --- Beam Search - Variante 3 (haz=1500, pagoda=V3+V1, goal_anywhere=True) ---
Nivel: 0, Nodos en este nivel: 1, Nodos expandidos hasta ahora: 0
Nivel: 1, Nodos en este nivel: 4, Nodos expandidos hasta ahora: 1
Nivel: 2, Nodos en este nivel: 14, Nodos expandidos hasta ahora: 5
Nivel: 3, Nodos en este nivel: 70, Nodos expandidos hasta ahora: 19
Nivel: 4, Nodos en este nivel: 372, Nodos expandidos hasta ahora: 89
Nivel: 5, Nodos en este nivel: 1500, Nodos expandidos hasta ahora: 461
Nivel: 6, Nodos en este nivel: 1500, Nodos expandidos hasta ahora: 1961
Nivel: 7, Nodos en este nivel: 1500, Nodos expandidos hasta ahora: 3461
Nivel: 8, Nodos en este nivel: 1500, Nodos expandidos hasta ahora: 4961
Nivel: 9, Nodos en este nivel: 1500, Nodos expandidos hasta ahora: 6461
Nivel: 10, Nodos en este nivel: 1500, Nodos expandidos hasta ahora: 7961
Nivel: 11, Nodos en este nivel: 1500, Nodos expandidos hasta ahora: 9461
Nivel: 12, Nodos en este nivel: 1500, Nodos expandidos hasta ahora: 10961
Nivel: 13, Nodos en este nivel: 1500, Nodos expandidos hasta ahora: 12461
Nivel: 14, Nodos en este nivel: 1500, Nodos expandidos hasta ahora: 13961
Nivel: 15, Nodos en este nivel: 1500, Nodos expandidos hasta ahora: 15461
Nivel: 16, Nodos en este nivel: 1500, Nodos expandidos hasta ahora: 16961
Nivel: 17, Nodos en este nivel: 1500, Nodos expandidos hasta ahora: 18461
Nivel: 18, Nodos en este nivel: 1500, Nodos expandidos hasta ahora: 19961
Nivel: 19, Nodos en este nivel: 1500, Nodos expandidos hasta ahora: 21461
Nivel: 20, Nodos en este nivel: 1500, Nodos expandidos hasta ahora: 22961
Nivel: 21, Nodos en este nivel: 1500, Nodos expandidos hasta ahora: 24461
Nivel: 22, Nodos en este nivel: 1500, Nodos expandidos hasta ahora: 25961
Nivel: 23, Nodos en este nivel: 1500, Nodos expandidos hasta ahora: 27461
Nivel: 24, Nodos en este nivel: 1500, Nodos expandidos hasta ahora: 28961
Nivel: 25, Nodos en este nivel: 1500, Nodos expandidos hasta ahora: 30461
Nivel: 26, Nodos en este nivel: 1500, Nodos expandidos hasta ahora: 31961
Nivel: 27, Nodos en este nivel: 1500, Nodos expandidos hasta ahora: 33461
Nivel: 28, Nodos en este nivel: 1500, Nodos expandidos hasta ahora: 34961
Nivel: 29, Nodos en este nivel: 1500, Nodos expandidos hasta ahora: 36461
Nivel: 30, Nodos en este nivel: 1500, Nodos expandidos hasta ahora: 37961
Nivel: 31, Nodos en este nivel: 1255, Nodos expandidos hasta ahora: 39461
Nivel: 32, Nodos en este nivel: 845, Nodos expandidos hasta ahora: 40716
Nivel: 33, Nodos en este nivel: 433, Nodos expandidos hasta ahora: 41561
Nivel: 34, Nodos en este nivel: 161, Nodos expandidos hasta ahora: 41994
Nivel: 35, Nodos en este nivel: 37, Nodos expandidos hasta ahora: 42155
Nivel: 36, Nodos en este nivel: 3, Nodos expandidos hasta ahora: 42192

Solucion encontrada con Beam Search! Nodos expandidos total: 42194
Profundidad de la solucion (saltos): 37
  OK Solucion encontrada (V3+V1): 37 pasos en 203.510s

  ==================================================
  Plan - Variante 3
  ==================================================
  Paso 1: Saltar -> Pieza en c42 salta sobre c43 hacia c44
  Paso 2: Saltar -> Pieza en c63 salta sobre c53 hacia c43
  Paso 3: Saltar -> Pieza en c33 salta sobre c43 hacia c53
  Paso 4: Saltar -> Pieza en c13 salta sobre c23 hacia c33
  Paso 5: Saltar -> Pieza en c83 salta sobre c73 hacia c63
  Paso 6: Saltar -> Pieza en c63 salta sobre c53 hacia c43
  Paso 7: Saltar -> Pieza en c44 salta sobre c43 hacia c42
  Paso 8: Saltar -> Pieza en c46 salta sobre c45 hacia c44
  Paso 9: Saltar -> Pieza en c48 salta sobre c47 hacia c46
  Paso 10: Saltar -> Pieza en c65 salta sobre c55 hacia c45
  Paso 11: Saltar -> Pieza en c35 salta sobre c45 hacia c55
  Paso 12: Saltar -> Pieza en c15 salta sobre c25 hacia c35
  Paso 13: Saltar -> Pieza en c85 salta sobre c75 hacia c65
  Paso 14: Saltar -> Pieza en c65 salta sobre c55 hacia c45
  Paso 15: Saltar -> Pieza en c35 salta sobre c45 hacia c55
  Paso 16: Saltar -> Pieza en c51 salta sobre c52 hacia c53
  Paso 17: Saltar -> Pieza en c31 salta sobre c41 hacia c51
  Paso 18: Saltar -> Pieza en c54 salta sobre c53 hacia c52
  Paso 19: Saltar -> Pieza en c56 salta sobre c55 hacia c54
  Paso 20: Saltar -> Pieza en c58 salta sobre c57 hacia c56
  Paso 21: Saltar -> Pieza en c33 salta sobre c34 hacia c35
  Paso 22: Saltar -> Pieza en c36 salta sobre c35 hacia c34
  Paso 23: Saltar -> Pieza en c38 salta sobre c37 hacia c36
  Paso 24: Saltar -> Pieza en c51 salta sobre c52 hacia c53
  Paso 25: Saltar -> Pieza en c32 salta sobre c42 hacia c52
  Paso 26: Saltar -> Pieza en c53 salta sobre c54 hacia c55
  Paso 27: Saltar -> Pieza en c34 salta sobre c44 hacia c54
  Paso 28: Saltar -> Pieza en c55 salta sobre c56 hacia c57
  Paso 29: Saltar -> Pieza en c36 salta sobre c46 hacia c56
  Paso 30: Saltar -> Pieza en c57 salta sobre c56 hacia c55
  Paso 31: Saltar -> Pieza en c55 salta sobre c54 hacia c53
  Paso 32: Saltar -> Pieza en c52 salta sobre c53 hacia c54
  Paso 33: Saltar -> Pieza en c14 salta sobre c24 hacia c34
  Paso 34: Saltar -> Pieza en c64 salta sobre c54 hacia c44
  Paso 35: Saltar -> Pieza en c34 salta sobre c44 hacia c54
  Paso 36: Saltar -> Pieza en c84 salta sobre c74 hacia c64
  Paso 37: Saltar -> Pieza en c64 salta sobre c54 hacia c44
  ==================================================

  OK Variante 3: plan validado (37 pasos, 1 pieza restante)

  --- Beam Search - Variante 5 (haz=3000, pagoda=V1+V2+V3, goal_anywhere=True) ---
Nivel: 0, Nodos en este nivel: 1, Nodos expandidos hasta ahora: 0
Nivel: 1, Nodos en este nivel: 4, Nodos expandidos hasta ahora: 1
Nivel: 2, Nodos en este nivel: 24, Nodos expandidos hasta ahora: 5
Nivel: 3, Nodos en este nivel: 120, Nodos expandidos hasta ahora: 29
Nivel: 4, Nodos en este nivel: 636, Nodos expandidos hasta ahora: 149
Nivel: 5, Nodos en este nivel: 3000, Nodos expandidos hasta ahora: 785
Nivel: 6, Nodos en este nivel: 3000, Nodos expandidos hasta ahora: 3785
Nivel: 7, Nodos en este nivel: 3000, Nodos expandidos hasta ahora: 6785
Nivel: 8, Nodos en este nivel: 3000, Nodos expandidos hasta ahora: 9785
Nivel: 9, Nodos en este nivel: 3000, Nodos expandidos hasta ahora: 12785
Nivel: 10, Nodos en este nivel: 3000, Nodos expandidos hasta ahora: 15785
Nivel: 11, Nodos en este nivel: 3000, Nodos expandidos hasta ahora: 18785
Nivel: 12, Nodos en este nivel: 3000, Nodos expandidos hasta ahora: 21785
Nivel: 13, Nodos en este nivel: 3000, Nodos expandidos hasta ahora: 24785
Nivel: 14, Nodos en este nivel: 3000, Nodos expandidos hasta ahora: 27785
Nivel: 15, Nodos en este nivel: 3000, Nodos expandidos hasta ahora: 30785
Nivel: 16, Nodos en este nivel: 3000, Nodos expandidos hasta ahora: 33785
Nivel: 17, Nodos en este nivel: 3000, Nodos expandidos hasta ahora: 36785
Nivel: 18, Nodos en este nivel: 3000, Nodos expandidos hasta ahora: 39785
Nivel: 19, Nodos en este nivel: 3000, Nodos expandidos hasta ahora: 42785
Nivel: 20, Nodos en este nivel: 3000, Nodos expandidos hasta ahora: 45785
Nivel: 21, Nodos en este nivel: 3000, Nodos expandidos hasta ahora: 48785
Nivel: 22, Nodos en este nivel: 3000, Nodos expandidos hasta ahora: 51785
Nivel: 23, Nodos en este nivel: 3000, Nodos expandidos hasta ahora: 54785
Nivel: 24, Nodos en este nivel: 3000, Nodos expandidos hasta ahora: 57785
Nivel: 25, Nodos en este nivel: 3000, Nodos expandidos hasta ahora: 60785
Nivel: 26, Nodos en este nivel: 3000, Nodos expandidos hasta ahora: 63785
Nivel: 27, Nodos en este nivel: 3000, Nodos expandidos hasta ahora: 66785
Nivel: 28, Nodos en este nivel: 3000, Nodos expandidos hasta ahora: 69785
Nivel: 29, Nodos en este nivel: 3000, Nodos expandidos hasta ahora: 72785
Nivel: 30, Nodos en este nivel: 3000, Nodos expandidos hasta ahora: 75785
Nivel: 31, Nodos en este nivel: 3000, Nodos expandidos hasta ahora: 78785
Nivel: 32, Nodos en este nivel: 2724, Nodos expandidos hasta ahora: 81785
Nivel: 33, Nodos en este nivel: 1574, Nodos expandidos hasta ahora: 84509
Nivel: 34, Nodos en este nivel: 628, Nodos expandidos hasta ahora: 86083
Nivel: 35, Nodos en este nivel: 175, Nodos expandidos hasta ahora: 86711
Nivel: 36, Nodos en este nivel: 42, Nodos expandidos hasta ahora: 86886

Busqueda (Haz) finalizada sin exito. Nodos expandidos total: 86928
  ! No se encontro solucion para Variante 5 con haz=3000, pagoda=V1+V2+V3 tras 597.8s

============================================================
  RESUMEN FINAL
------------------------------------------------------------
  OK Carga PDDL: COMPLETADO
  OK Validacion tableros: COMPLETADO
  OK Funcion pagoda: COMPLETADO
  OK Busqueda basica: COMPLETADO
  OK Beam Search: COMPLETADO

  ¡Todas las verificaciones superadas!
```

# Basic search
> **Nota**: *Se exlcuye del test general debido a su duración. Además, debido a la longitud desmedida de la salida por consola se omiten la gran mayoría de líneas de log ya que son realmente innecesarias y solo se usan para confirmar visualmente que el algoritmo sigue trabajando.*

```
Cargando dominio desde: C:\Users\Usuario\Senku-IA\PDDL\dominio_senku.pddl
Cargando problema desde: C:\Users\Usuario\Senku-IA\PDDL\problema_senku_tablero_clasico.pddl
Problema instanciado correctamente.

Iniciando Búsqueda en Profundidad (DFS)...
Nodos expandidos: 50, Frontera: 48
Nodos expandidos: 100, Frontera: 47
Nodos expandidos: 150, Frontera: 45
...
Nodos expandidos: 1929800, Frontera: 52
Nodos expandidos: 1929850, Frontera: 52
Nodos expandidos: 1929900, Frontera: 48

¡Solución encontrada! Nodos expandidos: 1929901
Profundidad de la solución (saltos): 31

========================================
SOLUCIÓN ENCONTRADA
========================================
Paso 1: Saltar -> Pieza en c46 salta sobre c45 hacia c44
Paso 2: Saltar -> Pieza en c43 salta sobre c44 hacia c45
Paso 3: Saltar -> Pieza en c41 salta sobre c42 hacia c43
Paso 4: Saltar -> Pieza en c64 salta sobre c54 hacia c44
Paso 5: Saltar -> Pieza en c56 salta sobre c55 hacia c54
Paso 6: Saltar -> Pieza en c53 salta sobre c54 hacia c55
Paso 7: Saltar -> Pieza en c44 salta sobre c45 hacia c46
Paso 8: Saltar -> Pieza en c65 salta sobre c55 hacia c45
Paso 9: Saltar -> Pieza en c73 salta sobre c63 hacia c53
Paso 10: Saltar -> Pieza en c75 salta sobre c74 hacia c73
Paso 11: Saltar -> Pieza en c43 salta sobre c53 hacia c63
Paso 12: Saltar -> Pieza en c73 salta sobre c63 hacia c53
Paso 13: Saltar -> Pieza en c23 salta sobre c33 hacia c43
Paso 14: Saltar -> Pieza en c35 salta sobre c34 hacia c33
Paso 15: Saltar -> Pieza en c37 salta sobre c36 hacia c35
Paso 16: Saltar -> Pieza en c57 salta sobre c47 hacia c37
Paso 17: Saltar -> Pieza en c14 salta sobre c24 hacia c34
Paso 18: Saltar -> Pieza en c43 salta sobre c53 hacia c63
Paso 19: Saltar -> Pieza en c51 salta sobre c52 hacia c53
Paso 20: Saltar -> Pieza en c63 salta sobre c53 hacia c43
Paso 21: Saltar -> Pieza en c43 salta sobre c33 hacia c23
Paso 22: Saltar -> Pieza en c31 salta sobre c32 hacia c33
Paso 23: Saltar -> Pieza en c34 salta sobre c33 hacia c32
Paso 24: Saltar -> Pieza en c13 salta sobre c23 hacia c33
Paso 25: Saltar -> Pieza en c32 salta sobre c33 hacia c34
Paso 26: Saltar -> Pieza en c34 salta sobre c35 hacia c36
Paso 27: Saltar -> Pieza en c15 salta sobre c25 hacia c35
Paso 28: Saltar -> Pieza en c45 salta sobre c35 hacia c25
Paso 29: Saltar -> Pieza en c37 salta sobre c36 hacia c35
Paso 30: Saltar -> Pieza en c25 salta sobre c35 hacia c45
Paso 31: Saltar -> Pieza en c46 salta sobre c45 hacia c44
========================================

Tiempo de ejecución: 5428.8179 segundos.
```