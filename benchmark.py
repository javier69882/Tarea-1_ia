import csv
import statistics
import matplotlib.pyplot as plt
import os
import sys
import time
from entorno.grilla import Mapa
from simulacion import ejecutar_simulacion_genetica

#silencia print durante las 150 iteraciones del benchmark para no saturar la consola
class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

def graficar_resultados(nombre, mapa, turnos, supervivencia):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # (Estadísticos de tiempo)
    ax1.hist(turnos, bins=15, color='skyblue', edgecolor='black')
    ax1.set_title(f'Distribución de Turnos de Evacuación\n({nombre} - Mapa {mapa})')
    ax1.set_xlabel('Total de Turnos hasta vaciar edificio')
    ax1.set_ylabel('Frecuencia (Iteraciones)')
    
    # Boxplot de supervivencia 
    ax2.boxplot(supervivencia, vert=True, patch_artist=True, boxprops=dict(facecolor='lightgreen'))
    ax2.set_title(f'Tasa de Supervivencia\n({nombre} - Mapa {mapa})')
    ax2.set_ylabel('Supervivencia (%)')
    ax2.set_xticks([1])
    ax2.set_xticklabels([nombre])
    
    # Ajustar diseño y guardar en la nueva carpeta 'imagenes'
    plt.tight_layout()
    plt.savefig(f"imagenes/graficos_{nombre}_mapa{mapa}.png")
    plt.close()

def ejecutar_benchmark(nombre_algoritmo, funcion_simulacion, tipo_mapa, iteraciones=200):
    print(f"\n[*] Iniciando Benchmark para '{nombre_algoritmo}' en Mapa {tipo_mapa} ({iteraciones} iteraciones)...")
    print("[*] Esto puede tomar un momento. Calculando...")
    
    resultados_turnos = []
    resultados_supervivencia = []
    
    # Inicio el cronometro
    tiempo_inicio = time.time()
    
    for i in range(iteraciones):
        print(f"\rProgreso: {i+1}/{iteraciones} completado...", end="")
        
        mapa = Mapa(tipo_mapa=tipo_mapa, filas=15, columnas=15)
        
        with HiddenPrints():
            historial = funcion_simulacion(mapa)
        
        if historial:
            estado_final = historial[-1]['agentes']
            total_agentes = len(estado_final)
            escapados = sum(1 for a in estado_final if a['estado'] == 'escapo')
            
            tasa_supervivencia = (escapados / total_agentes) * 100
            turnos = len(historial) - 1 
        else:
            tasa_supervivencia = 0.0
            turnos = 0
            
        resultados_turnos.append(turnos)
        resultados_supervivencia.append(tasa_supervivencia)

    # Detengo el cronómetro y calculo el tiempo total
    tiempo_fin = time.time()
    tiempo_total_segundos = tiempo_fin - tiempo_inicio
    
    print("\n[+] Benchmark finalizado.")
    
    if not resultados_turnos:
        print("[!] Error: No se obtuvieron resultados válidos.")
        return

    # Cálculos estadísticos
    media_turnos = statistics.mean(resultados_turnos)
    desviacion_turnos = statistics.stdev(resultados_turnos) if iteraciones > 1 else 0
    min_turnos = min(resultados_turnos)
    max_turnos = max(resultados_turnos)
    media_supervivencia = statistics.mean(resultados_supervivencia)
    
    # Cálculo de tiempo promedio en milisegundos
    tiempo_medio_ms = (tiempo_total_segundos / iteraciones) * 1000

    os.makedirs("resultados", exist_ok=True)
    os.makedirs("imagenes", exist_ok=True)
    
    iteraciones_exitosas = len(resultados_turnos)

    # Generar CSV
    archivo_csv = f"resultados/benchmark_{nombre_algoritmo}_mapa{tipo_mapa}.csv"
    with open(archivo_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Iteracion", "Turnos_Totales", "Tasa_Supervivencia(%)"])
        for i in range(iteraciones_exitosas):
            writer.writerow([i+1, resultados_turnos[i], resultados_supervivencia[i]])
            
    # Guardar resumen estadístico con las métricas de tiempo
    archivo_txt = f"resultados/resumen_{nombre_algoritmo}_mapa{tipo_mapa}.txt"
    with open(archivo_txt, mode='w') as file:
        file.write(f"--- RESUMEN ESTADÍSTICO ({nombre_algoritmo} - Mapa {tipo_mapa}) ---\n")
        file.write(f"Iteraciones completadas con éxito: {iteraciones_exitosas} de {iteraciones}\n\n")
        
        file.write(f"METRICAS DE RENDIMIENTO COMPUTACIONAL:\n")
        file.write(f"- Tiempo total de ejecución: {tiempo_total_segundos:.2f} segundos\n")
        file.write(f"- Tiempo medio por simulación: {tiempo_medio_ms:.2f} milisegundos\n\n")
        
        file.write(f"METRICAS DE SUPERVIVENCIA:\n")
        file.write(f"- Supervivencia media: {media_supervivencia:.2f}%\n\n")
        
        file.write(f"ESTADISTICOS DE TIEMPO (TURNOS):\n")
        file.write(f"- Media: {media_turnos:.2f} turnos\n")
        file.write(f"- Desviación estándar: {desviacion_turnos:.2f}\n")
        file.write(f"- Valor mínimo: {min_turnos} turnos\n")
        file.write(f"- Valor máximo: {max_turnos} turnos\n")

    # Generar gráficas 
    graficar_resultados(nombre_algoritmo, tipo_mapa, resultados_turnos, resultados_supervivencia)
    print(f"\n[*] ¡Éxito! CSV/TXT guardados en 'resultados/' e imágenes en 'imagenes/'.")