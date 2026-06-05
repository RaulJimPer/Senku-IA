import os
from unified_planning.io import PDDLReader

class SenkuPDDLReader:
    def __init__(self, domain_path: str, problem_path: str):
        self.domain_path = domain_path
        self.problem_path = problem_path
        self.problem = None

    def read_problem(self):
        reader = PDDLReader()
        self.problem = reader.parse_problem(self.domain_path, self.problem_path)
        return self.problem

    def cargar_fluentes(self):
        if self.problem is None:
            self.read_problem()
            
        fluentes_iniciales = self.problem.initial_values
        
        fluentes_activos = {}
        for fluente, valor in fluentes_iniciales.items():
            if valor.is_true():
                fluentes_activos[fluente] = valor
                
        return fluentes_activos

    def obtener_acciones_aplicables(self):
        if self.problem is None:
            self.read_problem()

        return self.problem.actions

    def _extraer_coordenadas(self, fluente):
        """
        Extrae el nombre de la casilla (ej. 'c31') de un fluente,
        tanto si es un objeto fluent de UP como si es un string 'pieza(c31)'.
        Retorna None si no es un fluente de pieza.
        """
        if isinstance(fluente, str):
            if not fluente.startswith("pieza("):
                return None
            return fluente[6:-1]
        else:
            if fluente.fluent().name != 'pieza':
                return None
            return str(fluente.args[0])

    def funcion_pagoda(self, fluentes_activos, variante=1):
        """
        Calcula el valor de la función pagoda para un estado dado.
        Existen distintas variantes de la función pagoda para Senku, 
        basadas en asignar un 1 a ciertas casillas y 0 a las demás.
        
        :param fluentes_activos: Iterable de fluentes activos (objetos UP o strings 'pieza(cXX)')
        :param variante: 1, 2 o 3, correspondiente a distintas asignaciones de pagoda
        :return: Valor total (entero)
        """
        suma = 0
        for fluente in fluentes_activos:
            casilla = self._extraer_coordenadas(fluente)
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

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    domain_path = os.path.join(base_dir, "..", "PDDL", "dominio_senku.pddl")
    problem_path = os.path.join(base_dir, "..", "PDDL", "problema_senku_tablero_clasico.pddl")

    lector_senku = SenkuPDDLReader(domain_path, problem_path)
    
    try:
        fluentes = lector_senku.cargar_fluentes()
        print(f"Fluentes cargados: {len(fluentes)}")
        
        acciones = lector_senku.obtener_acciones_aplicables()
        for accion in acciones:
            print(f"Acción: {accion.name} - Params: {[p.name for p in accion.parameters]}")
            
    except Exception as e:
        print(f"Error: {e}")
