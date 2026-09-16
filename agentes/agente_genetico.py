from algoritmos.genetico import AlgoritmoGenetico
from agentes.agente_base import AgenteBase

class AgenteGenetico(AgenteBase):
    def replanificar(self, mapa):
        if self.estado != 'vivo':
            return
        genetico = AlgoritmoGenetico(mapa=mapa, inicio=(self.fila, self.col), objetivo=self.objetivo, tam_poblacion=80, longitud_adn=20)
        self.ruta_planeada = genetico.evolucionar(generaciones=200).adn

    # Se sobrescribe el método padre porque las bacterias se mueven distinto, se modifica el fitness
    def mover(self, mapa):
        if self.estado != 'vivo' or not self.ruta_planeada:
            return
        gen_actual = self.ruta_planeada.pop(0) 
        movimientos = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1), 4: (0, 0)}
        df, dc = movimientos[gen_actual]
        nueva_fila, nueva_col = self.fila + df, self.col + dc
        
        if 0 <= nueva_fila < mapa.filas and 0 <= nueva_col < mapa.columnas:
            if mapa.matriz[nueva_fila][nueva_col].estado != 'm':
                mapa.matriz[self.fila][self.col].ocupacion = max(0, mapa.matriz[self.fila][self.col].ocupacion - 1)
                self.fila, self.col = nueva_fila, nueva_col
                mapa.matriz[self.fila][self.col].ocupacion += 1
                
        if mapa.matriz[self.fila][self.col].estado == 'f':
            self.estado = 'muerto'
            mapa.matriz[self.fila][self.col].ocupacion -= 1 
        elif (self.fila, self.col) == self.objetivo:
            self.estado = 'escapo'
            mapa.matriz[self.fila][self.col].ocupacion -= 1