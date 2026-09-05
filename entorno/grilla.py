import random
from entorno.celda import Celda

class Mapa:
    def __init__(self, filas=10, columnas=10):
        self.filas = filas
        self.columnas = columnas
        self.matriz = []
        for i in range(self.filas):
            fila_actual = []
            for j in range(self.columnas):
                fila_actual.append(Celda(estado='d'))
            self.matriz.append(fila_actual)

        self._generar_entorno_basico()

    def _generar_entorno_basico(self):
        plantilla = [
            ['m', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm'],
            ['m', 'd', 'd', 'd', 'm', 'd', 'd', 'm', 'd', 'm'],
            ['m', 'm', 'm', 'd', 'm', 'd', 'd', 'm', 'd', 'm'],
            ['m', 'd', 'd', 'd', 'm', 'd', 'd', 'm', 'd', 'm'],
            ['m', 'd', 'd', 'd', 'm', 'm', 'd', 'm', 'd', 'm'],
            ['m', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'm'],
            ['m', 'm', 'm', 'm', 'd', 'd', 'd', 'd', 'd', 'm'],
            ['m', 'd', 'd', 'm', 'd', 'm', 'm', 'm', 'm', 'm'],
            ['m', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'm'],
            ['m', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm'] 
        ]
        
        # Cargamos la plantilla
        for i in range(self.filas):
            for j in range(self.columnas):
                self.matriz[i][j].estado = plantilla[i][j]

        #fuego al aazar
        f_fila = random.randint(0, self.filas - 1)
        f_col = random.randint(0, self.columnas - 1)
        self.matriz[f_fila][f_col].estado = 'f'

    def propagar_fuego(self):
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        fuegos_con_espacio = []

        #Encontrar todos los fuegos que tienen al menos un vecino válido para quemar
        for f in range(self.filas):
            for c in range(self.columnas):
                if self.matriz[f][c].estado == 'f':
                    vecinos_validos = []
                    for df, dc in direcciones:
                        nf, nc = f + df, c + dc
                        #Si está dentro de los límites y es 'd' (disponible) o 'm' (muro)
                        if 0 <= nf < self.filas and 0 <= nc < self.columnas:
                            if self.matriz[nf][nc].estado in ['d', 'm']:
                                vecinos_validos.append((nf, nc))
                    
                    #Si este fuego tiene hacia donde expandirse, lo guardamos
                    if vecinos_validos:
                        fuegos_con_espacio.append(vecinos_validos)

        #Si hay fuegos que se pueden expandir, elegimos uno al azar
        if fuegos_con_espacio:
            # Elegimos al azar una lista de vecinos válidos 
            opciones_expansion = random.choice(fuegos_con_espacio)
            
            #De esas opciones, elegimos una casilla al azar para quemar
            nf, nc = random.choice(opciones_expansion)
            self.matriz[nf][nc].estado = 'f'

    def mostrar_mapa(self):
        for fila in self.matriz:
            print(" ".join(str(celda) for celda in fila))
        print("-" * 20)