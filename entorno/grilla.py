import random
from entorno.celda import Celda

class Mapa:
 
    def __init__(self, tipo_mapa=1, filas=15, columnas=15):
        self.filas = filas
        self.columnas = columnas
        self.tipo_mapa = tipo_mapa
        self.matriz = []
        
        for i in range(self.filas):
            fila_actual = []
            for j in range(self.columnas):
                fila_actual.append(Celda(estado='d'))
            self.matriz.append(fila_actual)
            
        self._generar_entorno_basico(self.tipo_mapa)

    def _generar_entorno_basico(self, tipo_mapa):
        if tipo_mapa == 1:
            # MAPA 1: Alta densidad / Cuello de botella severo
            plantilla = [
                ['m','m','m','m','m','m','m','m','m','m','m','m','m','m','m'],
                ['m','s','d','d','d','d','d','m','m','m','d','d','d','s','m'], # Inicio (s) en (1,1) y (1,13)
                ['m','d','s','s','d','d','d','m','m','m','d','s','s','s','m'],
                ['m','d','d','d','d','d','d','m','m','m','d','d','d','s','m'],
                ['m','d','d','s','d','d','d','s','d','d','d','s','s','d','m'], # Inicio (s) en (4,3) y (4,12)
                ['m','m','m','m','m','m','d','d','d','m','m','m','m','m','m'],
                ['m','m','m','m','m','m','s','d','s','m','m','m','m','m','m'],
                ['m','m','m','m','m','m','d','s','d','m','m','m','m','m','m'],# Inicio (s) en (7,7)
                ['m','m','m','m','m','m','d','d','d','m','m','m','m','m','m'],
                ['m','m','m','m','m','m','m','d','m','m','m','m','m','m','m'], # Inicia cuello de botella
                ['m','m','m','m','m','m','m','d','m','m','m','m','m','m','m'],
                ['m','m','m','m','m','m','m','s','m','m','m','m','m','m','m'],
                ['m','m','m','m','m','m','m','d','m','m','m','m','m','m','m'],
                ['m','m','m','m','m','m','m','g','m','m','m','m','m','m','m'], # Salida (g) en (13,7)
                ['m','m','m','m','m','m','m','m','m','m','m','m','m','m','m']
            ]
        elif tipo_mapa == 2:
            # MAPA 2: Densidad media / Laberinto corporativo
            plantilla = [
                ['m','m','m','m','m','m','m','m','m','m','m','m','m','m','m'],
                ['m','s','d','m','d','d','d','m','s','s','d','m','d','s','m'],  # Inicio (s) en (1,1), (1,8) y (1,13)
                ['m','d','d','m','d','m','d','m','m','m','d','m','d','d','m'],
                ['m','d','m','m','d','m','d','d','s','m','d','m','m','d','m'],
                ['m','d','d','d','d','m','m','m','d','m','d','d','d','d','m'],
                ['m','m','m','m','d','d','d','m','d','m','m','m','m','d','m'],   # Inicio (s) en (5,6)
                ['m','d','d','d','d','m','m','m','d','d','d','d','m','d','m'],
                ['m','d','m','m','m','m','d','m','m','d','m','d','m','d','m'],
                ['m','d','d','s','d','s','d','d','s','d','m','s','m','d','m'],  # Inicio (s)  en (8,3)
                ['m','d','m','m','m','m','m','m','m','d','m','d','m','d','m'],
                ['m','d','s','d','d','d','d','d','m','d','m','d','s','d','m'],
                ['m','m','m','m','m','m','m','d','m','d','m','m','m','m','m'],
                ['m','s','s','s','d','d','d','d','d','d','d','s','d','g','m'],   # Inicio (s) en (12,1) y Salida (g) en (12,13)
                ['m','m','m','m','m','m','m','m','m','m','m','m','m','m','m'],
                ['m','m','m','m','m','m','m','m','m','m','m','m','m','m','m']
            ]
        else:
            # MAPA 3: Baja densidad / Dispersión abierta
            plantilla = [
                ['m','m','m','m','m','m','m','m','m','m','m','m','m','m','m'],
                ['m','s','d','d','d','d','d','d','s','d','d','d','d','s','m'],    # Inicio (s) en (1,1) y (1,13)
                ['m','d','d','m','d','d','d','d','m','m','d','d','d','d','m'],
                ['m','d','d','d','d','d','s','d','d','d','d','m','d','d','m'],    # Inicio (s) en (3,6)
                ['m','d','m','d','d','d','d','d','d','d','d','d','d','d','m'],
                ['m','d','d','d','m','m','d','d','d','m','d','d','m','d','m'],
                ['m','s','d','d','d','d','d','d','d','d','d','d','d','d','m'],    # Inicio (s) en (6,1)
                ['m','d','d','m','d','d','d','s','d','d','m','d','d','d','m'],    # Inicio (s) en (7,7)
                ['m','d','d','s','d','m','d','d','d','s','d','d','s','d','m'],     # Inicio (s) en (8,12)
                ['m','d','s','d','d','d','d','d','d','s','m','d','d','d','m'],
                ['m','m','d','m','d','d','m','m','d','d','d','d','d','d','m'],
                ['m','d','d','d','d','d','d','d','d','d','d','d','m','d','m'],
                ['m','d','s','d','d','m','d','d','s','d','d','d','d','g','m'],    # Inicio (s) en (11,2) y (11,8) y Salida (g) en (12,13)
                ['m','d','s','d','d','d','d','d','d','d','d','s','d','d','m'],
                ['m','m','m','m','m','m','m','m','m','m','m','m','m','m','m']
            ]

        # Cargo la plantilla
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
        #Encontrar todos los fuegos que tienen al menos un vecino v lido para quemar
        for f in range(self.filas):
            for c in range(self.columnas):
                if self.matriz[f][c].estado == 'f':
                    vecinos_validos = []
                    for df, dc in direcciones:
                        nf, nc = f + df, c + dc
                        #Si esta  dentro de los limites y es 'd' (disponible) o 'm' (muro), o s o g
                        if 0 <= nf < self.filas and 0 <= nc < self.columnas:
                            if self.matriz[nf][nc].estado in ['d', 'm', 's', 'g']:
                                vecinos_validos.append((nf, nc))
                                        
                    #Si este fuego tiene hacia donde expandirse, lo guardamos
                    if vecinos_validos:
                        fuegos_con_espacio.append(vecinos_validos)
                        
        #Si hay fuegos que se pueden expandir, elegimos uno al azar
        if fuegos_con_espacio:
            # Elegimos al azar una lista de vecinos v lidos 
            opciones_expansion = random.choice(fuegos_con_espacio)
                        
            #De esas opciones, elegimos una casilla al azar para quemar
            nf, nc = random.choice(opciones_expansion)
            self.matriz[nf][nc].estado = 'f'

    def mostrar_mapa(self):
        for fila in self.matriz:
            print(" ".join(str(celda) for celda in fila))
        print("-" * 20)