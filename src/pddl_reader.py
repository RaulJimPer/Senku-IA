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

    def funcion_pagoda(self, fluentes_activos, variante=1):
        """
        Calcula el valor de la función pagoda para un estado dado.
        Existen distintas variantes de la función pagoda para Senku, 
        basadas en asignar un 1 a ciertas casillas y 0 a las demás.
        
        :param fluentes_activos: Diccionario o iterable de fluentes activos en el estado
        :param variante: 1, 2 o 3, correspondiente a distintas asignaciones de pagoda
        :return: Valor total (entero)
        """
        suma = 0
        for fluente in fluentes_activos:
            # Solo nos interesan las casillas ocupadas por una pieza
            if fluente.fluent().name == 'pieza':
                casilla = str(fluente.args[0])
                if len(casilla) == 3 and casilla.startswith('c'):
                    x = int(casilla[1])
                    y = int(casilla[2])
                    
                    if variante == 1:
                        # Variante 1: 1 si 'x' e 'y' son impares
                        if x % 2 == 1 and y % 2 == 1:
                            suma += 1
                    elif variante == 2:
                        # Variante 2: 1 si 'x' e 'y' son pares
                        if x % 2 == 0 and y % 2 == 0:
                            suma += 1
                    elif variante == 3:
                        # Variante 3: 1 si 'x' es par e 'y' es impar
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
        
        pagoda_v1 = lector_senku.funcion_pagoda(fluentes, variante=1)
        pagoda_v2 = lector_senku.funcion_pagoda(fluentes, variante=2)
        pagoda_v3 = lector_senku.funcion_pagoda(fluentes, variante=3)
        print(f"Pagoda V1: {pagoda_v1}")
        print(f"Pagoda V2: {pagoda_v2}")
        print(f"Pagoda V3: {pagoda_v3}")
        
        acciones = lector_senku.obtener_acciones_aplicables()
        for accion in acciones:
            print(f"Acción: {accion.name} - Params: {[p.name for p in accion.parameters]}")
            
    except Exception as e:
        print(f"Error: {e}")
