from algoritmos.informada.greedy import AlgoritmoGreedy
from agentes.agente_base import AgenteBase

class AgenteGreedy(AgenteBase):
    def replanificar(self, mapa):
        if self.estado != 'vivo':
            return
            
        greedy = AlgoritmoGreedy(mapa, (self.fila, self.col), self.objetivo)
        self.ruta_planeada = greedy.buscar_ruta()