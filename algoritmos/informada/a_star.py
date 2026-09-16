import heapq
#Muy similar a dijkstra, pero con heurística. Se utiliza una cola de prioridad para explorar los nodos con menor costo total (g + h) primero.

class AlgoritmoAStar:
    def __init__(self, mapa, inicio, objetivo, max_ocupacion=3):
        self.mapa = mapa
        self.inicio = inicio
        self.objetivo = objetivo
        self.max_ocupacion = max_ocupacion

    def heuristica(self, posicion):
        #distancia Manhattan
        return abs(posicion[0] - self.objetivo[0]) + abs(posicion[1] - self.objetivo[1])

    def buscar_ruta(self):

        heap = []
        contador = 0

        #estado inicio
        g_inicial = 0 #costo real
        f_inicial = g_inicial + self.heuristica(self.inicio) 
        heapq.heappush(heap, (f_inicial, contador, g_inicial, self.inicio, []))

        # Diccionario para guardar el costo g(n) más barato con el que hemos llegado a una celda
        costo_g = {self.inicio: 0}
        
        movimientos = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1), 4: (0, 0)}

        while heap:
            _, _, g_actual, actual, ruta = heapq.heappop(heap)

            # Si llegamos a la meta, retornamos la ruta exacta
            if actual == self.objetivo:
                return ruta

            # Explorar vecinos
            for gen_mov, (df, dc) in movimientos.items():
                nf, nc = actual[0] + df, actual[1] + dc
                vecino = (nf, nc)

                if 0 <= nf < self.mapa.filas and 0 <= nc < self.mapa.columnas:
                    estado_celda = self.mapa.matriz[nf][nc].estado
                    
                    if estado_celda not in ['m', 'f']:
                        nuevo_g = g_actual + 1 
                        
                        if vecino not in costo_g or nuevo_g < costo_g[vecino]:
                            costo_g[vecino] = nuevo_g
                            f_vecino = nuevo_g + self.heuristica(vecino)
                            
                            nueva_ruta = ruta + [gen_mov]
                            contador += 1
                            heapq.heappush(heap, (f_vecino, contador, nuevo_g, vecino, nueva_ruta))
                            
        # Si está rodeado de fuego o no hay salida
        return [4]