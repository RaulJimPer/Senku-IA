# Senku-IA

Proyecto sobre la planificacion automatica aplicada al Senku para la asignatura de Inteligencia Artificial (US).

## Estructura del repositorio

```
.
├── docs/
│   ├── memoria.tex          # Memoria del proyecto en LaTeX
│   ├── presentacion.pdf     # Presentacion del proyecto
│   ├── Rules.md             # Normas y descripcion del Senku
│   └── outputs.md           # Salidas de terminal de la bateria de pruebas
│
├── PDDL/
│   ├── dominio_senku.pddl
│   ├── problema_senku_prueba.pddl           # Tablero de prueba (3 piezas)
│   ├── problema_senku_tablero_clasico.pddl
│   ├── problema_senku_tablero_variante1.pddl
│   ├── problema_senku_tablero_variante3.pddl
│   └── problema_senku_tablero_variante5.pddl
│
├── src/
│   ├── pddl_reader.py       # Lectura de archivos PDDL
│   ├── helpers.py           # Nodo, fluentes, adyacencias, movimientos, hash
│   ├── basic_search.py      # Busqueda ciega (BFS / DFS)
│   ├── heuristic.py         # Funcion pagoda (V1, V2, V3) y heuristica
│   └── beam_search.py       # Busqueda en haz (Beam Search)
│
├── main.py                  # Punto de entrada unificado
└── README.md                # Guia basica
```

Presentación en Genially: https://view.genially.com/6a26eaff794c5b9cbbc92d60

## Ejecucion

Requiere Python 3.12+ y `unified-planning`. Entorno virtual recomendado:

```
python -m venv venv
venv\Scripts\activate    # Windows
pip install unified-planning
```

Punto de entrada: `main.py`

```
py ./main.py [argumentos]
```

### Modos

#### `--test`
Ejecuta la bateria completa de verificacion con las configuraciones optimas probadas:

| Tablero | Pagoda(s) | haz |
|---------|:---------:|:---:|
| Clasico | V1 | 500 |
| Variante 1 | V1+V3 | 1000 |
| Variante 3 | V3+V1 | 1500 |
| Variante 5 | V1+V2+V3 | 3000 |

```
py ./main.py --test
```

#### `--algoritmo {basic,beam}`
Ejecuta un algoritmo especifico sobre un tablero.

```
py ./main.py --algoritmo beam --tablero clasico --haz 500 --pagoda 1
py ./main.py --algoritmo basic --dfs --tablero variante1
```

### Argumentos

| Argumento | Descripcion |
|---|---|
| `--tablero {prueba,clasico,variante1,variante3,variante5}` | Tablero a resolver (defecto: `clasico`) |
| `--max-profundidad N` | Limite de profundidad (defecto: sin limite) |
| `--goal-especifico` | Usa el objetivo exacto del PDDL; por defecto se acepta 1 pieza en cualquier celda |

**Algoritmo basic:**
| Argumento | Descripcion |
|---|---|
| `--bfs` | Busqueda en anchura |
| `--dfs` | Busqueda en profundidad |

**Algoritmo beam:**
| Argumento | Descripcion |
|---|---|
| `--haz N` | Anchura del haz (defecto: 50) |
| `--pagoda {1,2,3}` | Variante primaria (defecto: 1) |
| `--pagoda-sec {1,2,3}` | Variante secundaria; defecto auto: 1->2, 2->3, 3->1 |
| `--pagoda-all` | Usa las tres variantes (V1+V2+V3) como clave de ordenacion |

### Ejemplos

```
py ./main.py --test

py ./main.py --algoritmo basic --dfs --tablero variante1

py ./main.py --algoritmo beam --tablero clasico --haz 500 --pagoda 1

py ./main.py --algoritmo beam --tablero variante3 --haz 1500 --pagoda 3 --pagoda-sec 1

py ./main.py --algoritmo beam --tablero variante5 --haz 3000 --pagoda-all

py ./main.py --help
```
