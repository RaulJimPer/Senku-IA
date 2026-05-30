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
