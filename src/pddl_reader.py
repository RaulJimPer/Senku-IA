from unified_planning.io import PDDLReader


class SenkuPDDLReader:
    """
    Lector de archivos PDDL de dominio y problema para el juego Senku.
    Utiliza la libreria Unified Planning para parsear los archivos y construir
    la representacion interna del problema.
    """

    def __init__(self, domain_path: str, problem_path: str):
        """
        :param domain_path: Ruta al archivo PDDL del dominio.
        :param problem_path: Ruta al archivo PDDL del problema (instancia).
        """
        self.domain_path = domain_path
        self.problem_path = problem_path
        self.problem = None

    def read_problem(self):
        """
        Parsea los archivos PDDL de dominio y problema y devuelve la
        instancia del problema lista para usar con el simulador de UP.

        :return: Instancia del problema (unified_planning.Problem).
        """
        reader = PDDLReader()
        self.problem = reader.parse_problem(self.domain_path, self.problem_path)
        return self.problem

    def cargar_fluentes(self):
        """
        Obtiene los fluentes activos (con valor True) del estado inicial del
        problema. El resultado incluye piezas, huecos y adyacencias.

        :return: Diccionario {fluente: valor} con los fluentes verdaderos.
        """
        if self.problem is None:
            self.read_problem()
        fluentes_iniciales = self.problem.initial_values
        fluentes_activos = {}
        for fluente, valor in fluentes_iniciales.items():
            if valor.is_true():
                fluentes_activos[fluente] = valor
        return fluentes_activos

    def obtener_acciones_aplicables(self):
        """
        Devuelve las acciones definidas en el dominio del problema.

        :return: Lista de objetos Action de UP.
        """
        if self.problem is None:
            self.read_problem()
        return self.problem.actions
