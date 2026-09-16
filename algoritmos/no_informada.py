from queue import Queue

class AlgoritmoBFS:
    def __init__(self, mapa, inicio, objetivo, max_ocupacion=3):
        self.mapa = mapa
        self.inicio = inicio
        self.objetivo = objetivo
        self.max_ocupacion = max_ocupacion # limite para lo de embotellamiento


    def buscar_ruta(self):
        cola= Queue()
        cola.put((self.inicio[0], self.inicio[1], []))  

        visitados = set()
        visitados.add(self.inicio)

        movimientos = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1), 4: (0, 0)}

        while not cola.empty():
            f_actual, c_actual, ruta = cola.get()

            #si llego a la meta, retorno la ruta 
            if (f_actual, c_actual) == self.objetivo:
                return ruta

            #exploro los vecinos en anchura
            for gen_mov,(df,dc) in movimientos.items():
                nf,nc=f_actual +df, c_actual + dc

                if 0 <= nf < self.mapa.filas and 0 <= nc < self.mapa.columnas:
                    estado_celda = self.mapa.matriz[nf][nc].estado
                    ocupacion = self.mapa.matriz[nf][nc].ocupacion

                    if estado_celda not in ['m', 'f']:
                        if (nf, nc) not in visitados:
                            visitados.add((nf, nc))
                            nueva_ruta = ruta + [gen_mov]
                            cola.put((nf, nc, nueva_ruta))
        #si la cola se vacia y no se encontro la salida, espera
        return [4]  # Movimiento de espera (no moverse)



class AlgoritmoDFS:
    def __init__(self, mapa, inicio, objetivo, max_ocupacion=3):
        self.mapa = mapa
        self.inicio = inicio
        self.objetivo = objetivo
        self.max_ocupacion = max_ocupacion

    def buscar_ruta(self):
        # Pila usando una lista 
        pila = []
        pila.append((self.inicio[0], self.inicio[1], []))
        
        visitados = set()
        visitados.add(self.inicio)
        
        # Mapeo de movimientos
        movimientos = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1), 4: (0, 0)}

        while pila:
            # Sacamos el ultimo elemento que entró a la pila
            f_actual, c_actual, ruta = pila.pop()

            # Si llegamos a la meta, retornamos la ruta exacta
            if (f_actual, c_actual) == self.objetivo:
                return ruta

            # Explorar vecinos en profundidad
            for gen_mov, (df, dc) in movimientos.items():
                nf, nc = f_actual + df, c_actual + dc

                if 0 <= nf < self.mapa.filas and 0 <= nc < self.mapa.columnas:
                    estado_celda = self.mapa.matriz[nf][nc].estado
                    
                    # Asumimos que el embotellamiento se disolverá 
                    if estado_celda not in ['m', 'f']:
                        if (nf, nc) not in visitados:
                            visitados.add((nf, nc))
                            nueva_ruta = ruta + [gen_mov]
                            pila.append((nf, nc, nueva_ruta))
                            
        # Si no hay salida posible
        return [4]