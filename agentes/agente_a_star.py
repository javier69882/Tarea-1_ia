from algoritmos.informada.a_star import AlgoritmoAStar
from agentes.agente_base import AgenteBase

class AgenteAStar(AgenteBase):
    def replanificar(self, mapa):
        if self.estado != 'vivo':
            return
            
        a_star = AlgoritmoAStar(mapa, (self.fila, self.col), self.objetivo)
        self.ruta_planeada = a_star.buscar_ruta()