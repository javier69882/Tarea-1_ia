from algoritmos.no_informada.dfs import AlgoritmoDFS
from agentes.agente_base import AgenteBase

class AgenteDFS(AgenteBase):
    def replanificar(self, mapa):
        if self.estado != 'vivo':
            return
        dfs = AlgoritmoDFS(mapa, (self.fila, self.col), self.objetivo)
        self.ruta_planeada = dfs.buscar_ruta()