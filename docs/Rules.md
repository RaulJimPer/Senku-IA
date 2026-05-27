# Análisis y Reglas del Senku (Peg Solitaire) para Modelado en PDDL

## 1. Reglas Universales del Senku
A la hora de definir las precondiciones y efectos de tus acciones en PDDL, debes aplicar de forma estricta las siguientes mecánicas del juego:

* **Configuración Inicial (Initial State):** La partida arranca con un tablero sobre el que existen un total de *M* piezas y, exclusivamente, un único hueco disponible. Habitualmente, este hueco original se encuentra en el centro geométrico del tablero.
* **Mecánica de Movimiento:** En cada turno, el jugador selecciona una pieza y debe hacerla "saltar" obligatoriamente por encima de una pieza adyacente, aterrizando sobre un hueco libre que esté inmediatamente después.
* **Restricción de Dirección:** Los saltos solo están permitidos en dirección **vertical u horizontal**. Los movimientos en diagonal están estrictamente prohibidos y supondrán un estado inválido.
* **Captura de Piezas:** La pieza sobre la que se acaba de realizar el salto es eliminada del tablero inmediatamente.
* **Condición de Victoria (Goal State):** El objetivo del rompecabezas es terminar la partida teniendo una única pieza sobre el tablero. Además, el objetivo definitivo más purista del Senku requiere que esa última pieza se posicione exactamente en la misma ubicación del hueco original  (versión que seguimos).

## 2. Tipos de Tableros Principales
Aunque tendremos que modelar tableros reducidos y versiones simplificadas (expuestos en la propuesta del proyecto), la base de comprensión debe partir de los tableros clásicos en los que se inspiran:
* **El Modelo Inglés (Tablero Clásico en Cruz):** Es el más habitual en el mundo anglosajón. Tiene forma de cruz griega asimétrica, conformada por brazos de 3x3 posiciones (un cuadrado central de 3x3 y cuatro rectángulos de 3x3 pegados), sumando 33 casillas o agujeros. 
* **El Modelo Europeo o Francés:** Tiene 37 posiciones. Sigue el patrón de cruz del tablero inglés, pero incorpora 4 posiciones extra situadas en las esquinas cóncavas interiores de la cruz. *Dato importante para pruebas:* Matemáticamente, este tablero no tiene solución si el hueco vacío inicial se sitúa en el puro centro.

## 3. Recursos Adicionales
Para visualizar bien el proceso algorítmico y entender los patrones que la Función Pagoda evaluará indirectamente, te será útil observar resoluciones en tiempo real:
* [Vídeo: Resolución rápida paso a paso del Senku (Tablero Inglés)](https://www.youtube.com/watch?v=x4d2q6yQ9kY)
* [Vídeo: Estrategia por zonas para ganar al Peg Solitaire](https://www.youtube.com/watch?v=_2UKhe1bg-Y)