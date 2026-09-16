import heapq

class AlgoritmoGreedy:
    def __init__(self, mapa, inicio, objetivo, max_ocupacion=3):
        self.mapa = mapa
        self.inicio = inicio
        self.objetivo = objetivo
        self.max_ocupacion = max_ocupacion

    def heuristica(self, posicion):
        # Distancia Manhattan
        return abs(posicion[0] - self.objetivo[0]) + abs(posicion[1] - self.objetivo[1])

    def buscar_ruta(self):
        heap = []
        contador = 0
        
        h_inicial = self.heuristica(self.inicio)
        heapq.heappush(heap, (h_inicial, contador, self.inicio, []))
        
        visitados = set()
        visitados.add(self.inicio)
        
        movimientos = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1), 4: (0, 0)}

        while heap:
            # Descartamos h_actual y el contador con guiones bajos
            _, _, actual, ruta = heapq.heappop(heap)

            if actual == self.objetivo:
                return ruta

            for gen_mov, (df, dc) in movimientos.items():
                nf, nc = actual[0] + df, actual[1] + dc
                vecino = (nf, nc)

                if 0 <= nf < self.mapa.filas and 0 <= nc < self.mapa.columnas:
                    estado_celda = self.mapa.matriz[nf][nc].estado
                    
                    if estado_celda not in ['m', 'f'] and vecino not in visitados:
                        visitados.add(vecino)
                        h_vecino = self.heuristica(vecino)
                        
                        nueva_ruta = ruta + [gen_mov]
                        contador += 1
                        # Push ordenando por la distancia heurística h(n)
                        heapq.heappush(heap, (h_vecino, contador, vecino, nueva_ruta))
                            
        return [4]