# Basic search
> **Nota**: *Debido a la longitud desmedida de la salida por consola se omiten la gran mayoría de líneas de log ya que son realmente innecesarias y solo se usan para confirmar visualmente que el algoritmo sigue trabajando.*

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