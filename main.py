from entorno.grilla import Mapa

print("Iniciando simulación del mapa...")
    
    # 1. Instanciamos la clase Mapa (esto crea la matriz 10x10 y aplica el entorno básico)
mi_mapa = Mapa(filas=10, columnas=10)
    
    # 2. Imprimimos el estado inicial (Turno 0)
print("Turno 0 (Estado Inicial):")
mi_mapa.mostrar_mapa()
    
    # 3. Simulamos varios turnos de propagación del fuego imprimiendo en pantalla
cantidad_turnos = 4
for turno in range(1, cantidad_turnos + 1):
    mi_mapa.propagar_fuego()
    print(f"Turno {turno} de propagación:")
    mi_mapa.mostrar_mapa()

