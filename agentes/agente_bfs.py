from algoritmos.no_informada.bfs import AlgoritmoBFS
from agentes.agente_base import AgenteBase

class AgenteBFS(AgenteBase):
    def replanificar(self, mapa):
        if self.estado != 'vivo':
            return
        bfs = AlgoritmoBFS(mapa, (self.fila, self.col), self.objetivo)
        self.ruta_planeada = bfs.buscar_ruta()