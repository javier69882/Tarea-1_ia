import os
import time
from benchmark import ejecutar_benchmark
from simulacion.motor import ejecutar_simulacion
from agentes.agente_bfs import AgenteBFS
from agentes.agente_dfs import AgenteDFS
from agentes.agente_genetico import AgenteGenetico
from entorno.grilla import Mapa

def limpiar_pantalla():
    #limpiar la consola
    os.system('cls' if os.name == 'nt' else 'clear')

def preguntar_visualizacion(historial):
    if historial:
        print("\n" + "-"*40)
        ver = input("¿Deseas reproducir la simulación con Pygame? (s/n): ")
        if ver.lower() == 's':
            import visualizador
            visualizador.reproducir(historial)

def visualizar_ruta(mapa, inicio, objetivo, adn):
    fila_actual, col_actual = inicio
    movimientos = {
        0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1), 4: (0, 0)
    }
    
    # Lista para guardar los estados originales y no arruinar el mapa
    historial_cambios = []
    
    for gen in adn:
        df, dc = movimientos[gen]
        nueva_fila, nueva_col = fila_actual + df, col_actual + dc
        
        if 0 <= nueva_fila < mapa.filas and 0 <= nueva_col < mapa.columnas:
            estado = mapa.matriz[nueva_fila][nueva_col].estado
            
            if estado == 'm':
                pass # Choca con un muro, se queda en el mismo lugar
            elif estado == 'f':
                break # Pisa fuego y muere, termina el trazado aquí
            else:
                # Movimiento válido
                fila_actual, col_actual = nueva_fila, nueva_col
                
                # Si la celda no es la de inicio ni la salida, la marcamos
                if (fila_actual, col_actual) not in [inicio, objetivo]:
                    # Guardamos el estado original si no lo hemos guardado antes
                    if not any(f == fila_actual and c == col_actual for f, c, _ in historial_cambios):
                        historial_cambios.append((fila_actual, col_actual, estado))
                    
                    # Marcamos la ruta con un asterisco
                    mapa.matriz[fila_actual][col_actual].estado = '*'
                    
        # Si llega a la salida, detenemos el trazado
        if (fila_actual, col_actual) == objetivo:
            break
            
    print("\n[*] Ruta trazada en el mapa (marcada con '*'):")
    mapa.mostrar_mapa()
    
    # Limpiamos el mapa restaurando los estados originales
    for f, c, estado_original in historial_cambios:
        mapa.matriz[f][c].estado = estado_original

def main():
    # Instanciamos el entorno de pruebas una sola vez al inicio
    mapa_actual = Mapa(filas=10, columnas=10)
    
    # Coordenadas de inicio ('s') y salida ('g') plantilla
    inicio = (1, 1)
    objetivo = (8, 8)

    while True:
        print("\n" + "="*40)
        print(" SIMULADOR DE EVACUACIÓN - TAREA 1")
        print("="*40)
        print(" Búsqueda No Informada:")
        print("   1. Ejecutar BFS (Búsqueda en Anchura) ")
        print("   2. Ejecutar DFS (Búsqueda en Profundidad) ")
        print("\n Búsqueda Informada:")
        print("   3. Ejecutar A* (A-Estrella) ")
        print("   4. Ejecutar Greedy Best-First Search ")
        print("\n Optimización Bioinspirada:")
        print("   5. Ejecutar Algoritmo Genético (Bacterias)")
        print("\n Herramientas de Visualización:")
        print("   6. Mostrar estado actual del mapa")
        print("   7. Simular propagación del fuego (1 turno)")
        print("   8. Reiniciar mapa al estado original")
        print("\n Benchmarking:")
        print("   9. Ejecutar Benchmark Estadístico Genético (200 iteraciones)")
        print("  10. Ejecutar Benchmark Estadístico BFS (200 iteraciones)")
        print("  11. Ejecutar Benchmark Estadístico DFS (200 iteraciones)")
        print("\n   0. Salir")
        print("="*40)
        
        opcion = input("Seleccione un modo de ejecución: ")

        tipo_mapa = 1 
        if opcion in ['1', '2', '3', '4', '5']:
            print("\nSeleccione el entorno de pruebas:")
            print("  1. Cuello de botella (Alta densidad)")
            print("  2. Laberinto corporativo (Densidad media)")
            print("  3. Dispersión abierta (Baja densidad)")
            seleccion_mapa = input("Opción (1-3): ")
            tipo_mapa = int(seleccion_mapa) if seleccion_mapa in ['1', '2', '3'] else 1
  
        match opcion:
            case '1':
                mapa_limpio = Mapa(tipo_mapa=tipo_mapa, filas=15, columnas=15)
                historial = ejecutar_simulacion(mapa_limpio, AgenteBFS, "BFS")
                preguntar_visualizacion(historial)
            
            case '2':
                mapa_limpio = Mapa(tipo_mapa=tipo_mapa, filas=15, columnas=15)
                historial = ejecutar_simulacion(mapa_limpio, AgenteDFS, "DFS")
                preguntar_visualizacion(historial)
            
            case '3':
                print("\n[!] Ejecutando A*... (Pendiente de implementar)")
            
            case '4':
                print("\n[!] Ejecutando Greedy... (Pendiente de implementar)")
            
            case '5':
                mapa_limpio = Mapa(tipo_mapa=tipo_mapa, filas=15, columnas=15)
                historial = ejecutar_simulacion(mapa_limpio, AgenteGenetico, "Genetico")
                preguntar_visualizacion(historial)

            case '6':
                print("\n[*] Mapa actual:")
                mapa_actual.mostrar_mapa()
            
            case '7':
                print("\n[*] El fuego se ha propagado 1 turno.")
                mapa_actual.propagar_fuego()
                mapa_actual.mostrar_mapa()
                
            case '8':
                print("\n[*] Reiniciando mapa...")
                mapa_actual = Mapa(filas=10, columnas=10)
                print("Mapa reiniciado a su estado original.")

            case '9':
                print("\n[*] Ejecutando Benchmark Estadístico completo (3 Mapas)...")
                for mapa_id in [1, 2, 3]:
                    print(f"\n--- INICIANDO MAPA {mapa_id} ---")
                    # Pasamos la clase AgenteGenetico al benchmark
                    ejecutar_benchmark("Genetico", AgenteGenetico, mapa_id)
                print("\n[+] Benchmarks de los 3 mapas completados exitosamente")

            case '10':
                print("\n[*] Ejecutando Benchmark Estadístico completo BFS (3 Mapas)...")
                for mapa_id in [1, 2, 3]:
                    print(f"\n--- INICIANDO MAPA {mapa_id} ---")
                    # Pasamos la clase AgenteBFS al benchmark
                    ejecutar_benchmark("BFS", AgenteBFS, mapa_id)
                print("\n[+] Benchmarks BFS de los 3 mapas completados exitosamente")

            case '11':
                print("\n[*] Ejecutando Benchmark Estadístico completo DFS (3 Mapas)...")
                for mapa_id in [1, 2, 3]:
                    print(f"\n--- INICIANDO MAPA {mapa_id} ---")
                    # Pasamos la clase AgenteDFS al benchmark
                    ejecutar_benchmark("DFS", AgenteDFS, mapa_id)
                print("\n[+] Benchmarks DFS de los 3 mapas completados exitosamente")
            
            case '0':
                print("\nSaliendo del simulador... ")
                break
                
            case _:
                print("\n[x] Opción no válida. Intente nuevamente.")
        
        input("\nPresione Enter para continuar...")
        limpiar_pantalla()

if __name__ == "__main__":
    main()