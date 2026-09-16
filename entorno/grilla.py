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
        archivo_mapa = f"mapas/mapa{tipo_mapa}.txt"
        
        try:
            with open(archivo_mapa, 'r') as file:
                # Leemos las líneas ignorando las que estén en blanco
                lineas = [linea.strip() for linea in file.readlines() if linea.strip()]
                
            for i in range(self.filas):
                # Limpiamos la línea de espacios para que quede un string continuo como "mmmmmm..."
                fila_limpia = lineas[i].replace(" ", "")
                
                for j in range(self.columnas):
                    self.matriz[i][j].estado = fila_limpia[j]
                    
        except FileNotFoundError:
            print(f"\n[!] Error crítico: No se encontró el archivo '{archivo_mapa}'.")
            print("[!] Asegúrate de que la carpeta 'mapas' exista en la raíz del proyecto.")
            
        # Generar fuego al azar
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