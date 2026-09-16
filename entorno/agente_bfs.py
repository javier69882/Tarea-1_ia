from algoritmos.no_informada import AlgoritmoBFS

class AgenteBFS:
    def __init__(self, id_agente, fila, col):
        self.id = id_agente
        self.fila = fila
        self.col = col
        self.estado = 'vivo' # Estados 'vivo', 'escapo', 'muerto'
        self.ruta_planeada = [] 
        self.objetivo = None

    @classmethod
    def spawnear_desde_mapa(cls, mapa):
        agentes_creados = []
        objetivo_encontrado = None
        id_contador = 1
        
        for f in range(mapa.filas):
            for c in range(mapa.columnas):
                estado_celda = mapa.matriz[f][c].estado
                if estado_celda == 's':
                    agentes_creados.append(cls(id_contador, f, c))
                    # Sumamos ocupación en el punto de inicio
                    mapa.matriz[f][c].ocupacion += 1
                    id_contador += 1
                elif estado_celda == 'g':
                    objetivo_encontrado = (f, c)
                    
        for agente in agentes_creados:
            agente.objetivo = objetivo_encontrado
            
        return agentes_creados, objetivo_encontrado

    def replanificar(self, mapa):
        """Usa Búsqueda en Anchura (BFS) para encontrar el camino más corto"""
        if self.estado != 'vivo':
            return
            
        bfs = AlgoritmoBFS(mapa, (self.fila, self.col), self.objetivo)
        self.ruta_planeada = bfs.buscar_ruta()

    def mover(self, mapa):
        if self.estado != 'vivo' or not self.ruta_planeada:
            return
            
        # Vemos cuál es el próximo paso sin sacarlo de la lista todavía
        paso_actual = self.ruta_planeada[0] 
        
        if paso_actual == 4:
            # Si el paso es esperar, lo consumimos y terminamos el turno
            self.ruta_planeada.pop(0)
            return

        movimientos = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}
        df, dc = movimientos[paso_actual]
        nueva_fila, nueva_col = self.fila + df, self.col + dc
        
        if 0 <= nueva_fila < mapa.filas and 0 <= nueva_col < mapa.columnas:
            estado_destino = mapa.matriz[nueva_fila][nueva_col].estado
            ocupacion_destino = mapa.matriz[nueva_fila][nueva_col].ocupacion
            
            if estado_destino == 'm':
                self.ruta_planeada = []
                return

            # EMBOTELLAMIENTO EN TIEMPO REAL
            if ocupacion_destino >= 3:
                # La casilla está llena. RETURN sin usar pop().
                # El agente se queda quieto y retendrá el mismo movimiento para el próximo turno.
                return
                
            # Si está libre, consumimos el movimiento de la lista
            self.ruta_planeada.pop(0)

            # Restamos ocupación de la celda que abandonamos
            mapa.matriz[self.fila][self.col].ocupacion -= 1
            mapa.matriz[self.fila][self.col].ocupacion = max(0, mapa.matriz[self.fila][self.col].ocupacion)
            
            # Actualizamos coordenadas
            self.fila = nueva_fila
            self.col = nueva_col
            
            # Sumamos ocupación a la nueva celda
            mapa.matriz[self.fila][self.col].ocupacion += 1
                
        # Revisar si pisó fuego al moverse
        if mapa.matriz[self.fila][self.col].estado == 'f':
            self.estado = 'muerto'
            mapa.matriz[self.fila][self.col].ocupacion -= 1 
        # Revisar si llegó a la salida
        elif (self.fila, self.col) == self.objetivo:
            self.estado = 'escapo'
            mapa.matriz[self.fila][self.col].ocupacion -= 1