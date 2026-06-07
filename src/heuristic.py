from src.helpers import filtrar_fluentes_relevantes


def extraer_coordenadas(fluente):
    """
    Extrae el nombre de la casilla (ej. 'c31') de un fluente, tanto si es
    un objeto fluent de UP como si es un string del tipo 'pieza(c31)'.

    :param fluente: Objeto fluent de UP o string 'pieza(cXX)'.
    :return: Nombre de la casilla (str) o None si no es un fluente de pieza.
    """
    if isinstance(fluente, str):
        if not fluente.startswith("pieza("):
            return None
        return fluente[6:-1]
    else:
        if fluente.fluent().name != 'pieza':
            return None
        return str(fluente.args[0])


def funcion_pagoda(fluentes_activos, variante=1):
    """
    Calcula el valor de la funcion pagoda para un estado dado. Asigna un peso
    de 1 a casillas especificas segun la variante y 0 al resto. Las variantes
    se basan en la paridad de las coordenadas (x, y) de cada casilla.

    :param fluentes_activos: Iterable de fluentes activos (objetos UP o strings).
    :param variante: 1, 2 o 3, correspondiente a distintas asignaciones de pagoda.
    :return: Valor total de la funcion pagoda (entero).
    """
    suma = 0
    for fluente in fluentes_activos:
        casilla = extraer_coordenadas(fluente)
        if casilla is None:
            continue
        if len(casilla) == 3 and casilla.startswith('c'):
            x = int(casilla[1])
            y = int(casilla[2])

            if variante == 1:
                if x % 2 == 1 and y % 2 == 1:
                    suma += 1
            elif variante == 2:
                if x % 2 == 0 and y % 2 == 0:
                    suma += 1
            elif variante == 3:
                if x % 2 == 0 and y % 2 == 1:
                    suma += 1

    return suma


def heuristica_senku(estado, cached_keys, variante_pagoda=1):
    """
    Heuristica para Senku basada en la funcion pagoda. Extrae los fluentes
    activos del estado y calcula la suma ponderada de las piezas segun la
    variante de pagoda seleccionada. Menor valor indica un estado mas cercano
    al objetivo (una unica pieza en una casilla de peso bajo).

    :param estado: Estado del simulador UP.
    :param cached_keys: Lista de fluentes relevantes (pieza/vacio).
    :param variante_pagoda: Variante de la funcion pagoda (1, 2 o 3).
    :return: Valor heuristico del estado (entero).
    """
    activos = []
    for fluente in cached_keys:
        try:
            val = estado.get_value(fluente)
            if val.is_true():
                activos.append(fluente)
        except Exception:
            pass

    return funcion_pagoda(activos, variante=variante_pagoda)
