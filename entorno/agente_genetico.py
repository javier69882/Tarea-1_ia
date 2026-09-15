from algoritmos.genetico import AlgoritmoGenetico

class AgenteGenetico:
    def __init__(self, id_agente, fila, col):
        self.id = id_agente
        self.fila = fila
        self.col = col
        self.estado = 'vivo' # Estados  'vivo', 'escapo', 'muerto'
        self.ruta_planeada = [] #  secuencia de genes/movimientos
        self.objetivo = None

    @classmethod
    
    def spawnear_desde_mapa(cls, mapa):
        agentes_creados = []
        objetivo_encontrado = None
        id_contador = 1
        """
         Lee el mapa, busca todas las 's' y crea un agente por cada una.
         También detecta dónde está la 'g' (salida) para asignarla como objetivo.
         """
        
        for f in range(mapa.filas):
            for c in range(mapa.columnas):
                estado_celda = mapa.matriz[f][c].estado
                if estado_celda == 's':
                    agentes_creados.append(cls(id_contador, f, c))
                    # Sumamo la ocupación en el punto de inicio
                    mapa.matriz[f][c].ocupacion += 1
                    id_contador += 1
                elif estado_celda == 'g':
                    objetivo_encontrado = (f, c)
                    
        for agente in agentes_creados:
            agente.objetivo = objetivo_encontrado
            
        return agentes_creados, objetivo_encontrado

    def replanificar(self, mapa):
        """Usa el Algoritmo Genético desde su posición ACTUAL para buscar la salida"""
        if self.estado != 'vivo':
            return
            
        genetico = AlgoritmoGenetico(
            mapa=mapa, 
            inicio=(self.fila, self.col), 
            objetivo=self.objetivo, 
            tam_poblacion=80, 
            longitud_adn=20 
        )
        # Evoluciona en silencio para encontrar la ruta
        mejor_bacteria = genetico.evolucionar(generaciones=200)
        self.ruta_planeada = mejor_bacteria.adn

    def mover(self, mapa):
        if self.estado != 'vivo' or not self.ruta_planeada:
            return
            
        gen_actual = self.ruta_planeada.pop(0) 
        movimientos = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1), 4: (0, 0)}
        df, dc = movimientos[gen_actual]
        nueva_fila, nueva_col = self.fila + df, self.col + dc
        
        if 0 <= nueva_fila < mapa.filas and 0 <= nueva_col < mapa.columnas:
            estado_destino = mapa.matriz[nueva_fila][nueva_col].estado
            if estado_destino != 'm':
                #Restamos ocupación de la celda que abandonamos
                mapa.matriz[self.fila][self.col].ocupacion -= 1
                mapa.matriz[self.fila][self.col].ocupacion = max(0, mapa.matriz[self.fila][self.col].ocupacion)
                
                #Actualizamos coordenadas
                self.fila = nueva_fila
                self.col = nueva_col
                
                #Sumamos ocupación a la nueva celda
                mapa.matriz[self.fila][self.col].ocupacion += 1
                
        # Revisar si pisó fuego al moverse
        if mapa.matriz[self.fila][self.col].estado == 'f':
            self.estado = 'muerto'
            # Liberar espacio porque el agente murió
            mapa.matriz[self.fila][self.col].ocupacion -= 1 
        # Revisar si llegó a la salida
        elif (self.fila, self.col) == self.objetivo:
            self.estado = 'escapo'
            mapa.matriz[self.fila][self.col].ocupacion -= 1