import os 
import time 
from entorno.agente_genetico import AgenteGenetico
from entorno.agente_bfs import AgenteBFS
from entorno.agente_dfs import AgenteDFS

def ejecutar_simulacion_genetica(mapa_actual):
    print("\n[*] Iniciando simulacion Dinamica con Agentes (Genetico)...")
    print("[*] Calculando rutas para Pygame..., por favor espera.")
    
    #El agente lee el mapa e instancia a las personas
    agentes, meta = AgenteGenetico.spawnear_desde_mapa(mapa_actual)
    
    if not agentes or not meta:
        print("[!] Error: No se encontr  inicio ('s') o meta ('g') en el mapa.")
        return None
                 
    k_turnos_fuego = 2 
    turno_actual = 1
    
    # Declaramos las variables de conteo iniciales para evitar errores si el bucle termina de golpe
    escapados = 0
    muertos = 0
    
    # Lista donde guardaremos los estados para pygame
    historial_simulacion = []
    
    while any(a.estado == 'vivo' for a in agentes):
        # os.system('cls' if os.name == 'nt' else 'clear')
        # print(f"\n--- TURNO {turno_actual} ---")
        
        # Visualizacion del estado actual (Ahora en lugar de imprimirlo, lo guardamos)
        estado_turno = {
            'mapa': [[celda.estado for celda in fila] for fila in mapa_actual.matriz],
            'agentes': [{'id': a.id, 'f': a.fila, 'c': a.col, 'estado': a.estado} for a in agentes]
        }
        historial_simulacion.append(estado_turno)
        
        # Replanificacion y Movimiento de los agentes
        for agente in agentes:
            if agente.estado == 'vivo':
                # Optimizamos para no replanificar cada turno si ya tiene ruta
                if not agente.ruta_planeada:
                    # Replanifica su ruta desde donde est  parado
                    agente.replanificar(mapa_actual)
                
                agente.mover(mapa_actual)
                         
        #Propagacion del fuego cada 'k' turnos
        if turno_actual % k_turnos_fuego == 0:
            mapa_actual.propagar_fuego()
            # print("\n[!]  EL FUEGO SE HA PROPAGADO!")
                         
            # Revisar si el nuevo fuego quemo a un agente que estaba quieto
            for agente in agentes:
                if agente.estado == 'vivo' and mapa_actual.matriz[agente.fila][agente.col].estado == 'f':
                    agente.estado = 'muerto'
                    # Liberar ocupación de la celda al morir
                    mapa_actual.matriz[agente.fila][agente.col].ocupacion = max(0, mapa_actual.matriz[agente.fila][agente.col].ocupacion - 1)
        
        
       
        
        # time.sleep(0.5) 
        turno_actual += 1
          
    # Guardar el último frame para que el final no se corte en pygame
    estado_final = {
        'mapa': [[celda.estado for celda in fila] for fila in mapa_actual.matriz],
        'agentes': [{'id': a.id, 'f': a.fila, 'c': a.col, 'estado': a.estado} for a in agentes]
    }
    historial_simulacion.append(estado_final)

    # Resumen de estados
    vivos = sum(1 for a in agentes if a.estado == 'vivo')
    escapados = sum(1 for a in agentes if a.estado == 'escapo')
    muertos = sum(1 for a in agentes if a.estado == 'muerto')
    print(f"\nAgentes vivos: {vivos} | Escaparon: {escapados} | Bajas: {muertos}")
          
    print("\n[+] SIMULACION FINALIZADA.")
    
    # M tricas requeridas por el marco de evaluaci
    tasa_supervivencia = (escapados / len(agentes)) * 100
    print(f"Tasa de Supervivencia: {tasa_supervivencia:.2f}%")
    
    return historial_simulacion

def ejecutar_simulacion_bfs(mapa_actual):

    print("\n[*] Iniciando simulación Dinámica con Agentes (BFS)...")
    
    agentes, meta = AgenteBFS.spawnear_desde_mapa(mapa_actual)
    
    if not agentes or not meta:
        print("[!] Error: No se encontró inicio ('s') o meta ('g') en el mapa.")
        return None
                 
    k_turnos_fuego = 2 
    turno_actual = 1
    escapados = 0
    muertos = 0
    historial_simulacion = []
    
    while any(a.estado == 'vivo' for a in agentes):
        #se termina si exede muchos turnos
        if turno_actual > 500:
            for a in agentes:
                if a.estado == 'vivo':
                    a.estado = 'muerto'
                    mapa_actual.matriz[a.fila][a.col].ocupacion = max(0, mapa_actual.matriz[a.fila][a.col].ocupacion - 1)
            break
        estado_turno = {
            'mapa': [[celda.estado for celda in fila] for fila in mapa_actual.matriz],
            'agentes': [{'id': a.id, 'f': a.fila, 'c': a.col, 'estado': a.estado} for a in agentes]
        }
        historial_simulacion.append(estado_turno)
        
        # Replanificación y Movimiento
        for agente in agentes:
            if agente.estado == 'vivo':
                # Replanificamos si se quedó sin ruta o si el siguiente paso se incendió
                if not agente.ruta_planeada:
                    agente.replanificar(mapa_actual)
                elif agente.ruta_planeada:
                    # Check de seguridad: si el próximo paso planeado ahora tiene fuego, recalcula
                    sig_paso = agente.ruta_planeada[0]
                    movs = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1), 4: (0, 0)}
                    df, dc = movs[sig_paso]
                    if mapa_actual.matriz[agente.fila + df][agente.col + dc].estado == 'f':
                        agente.replanificar(mapa_actual)

                agente.mover(mapa_actual)
                         
        # Propagación del fuego
        if turno_actual % k_turnos_fuego == 0:
            mapa_actual.propagar_fuego()
                         
            for agente in agentes:
                if agente.estado == 'vivo' and mapa_actual.matriz[agente.fila][agente.col].estado == 'f':
                    agente.estado = 'muerto'
                    mapa_actual.matriz[agente.fila][agente.col].ocupacion = max(0, mapa_actual.matriz[agente.fila][agente.col].ocupacion - 1)
        
        turno_actual += 1
          
    estado_final = {
        'mapa': [[celda.estado for celda in fila] for fila in mapa_actual.matriz],
        'agentes': [{'id': a.id, 'f': a.fila, 'c': a.col, 'estado': a.estado} for a in agentes]
    }
    historial_simulacion.append(estado_final)

    vivos = sum(1 for a in agentes if a.estado == 'vivo')
    escapados = sum(1 for a in agentes if a.estado == 'escapo')
    muertos = sum(1 for a in agentes if a.estado == 'muerto')
    print(f"\nAgentes vivos: {vivos} | Escaparon: {escapados} | Bajas: {muertos}")
          
    print("\n[+] SIMULACION FINALIZADA.")
    tasa_supervivencia = (escapados / len(agentes)) * 100
    print(f"Tasa de Supervivencia: {tasa_supervivencia:.2f}%")
    
    return historial_simulacion

def ejecutar_simulacion_dfs(mapa_actual):
    print("\n[*] Iniciando simulación Dinámica con Agentes (DFS)...")
    
    agentes, meta = AgenteDFS.spawnear_desde_mapa(mapa_actual)
    
    if not agentes or not meta:
        print("[!] Error: No se encontró inicio ('s') o meta ('g') en el mapa.")
        return None
                 
    k_turnos_fuego = 2 
    turno_actual = 1
    historial_simulacion = []
    
    while any(a.estado == 'vivo' for a in agentes):
        # se detiene si excede muchos turnos
        if turno_actual > 500:
            print("\n[!] Límite de 500 turnos. Agentes acorralados.")
            for a in agentes:
                if a.estado == 'vivo':
                    a.estado = 'muerto'
                    mapa_actual.matriz[a.fila][a.col].ocupacion = max(0, mapa_actual.matriz[a.fila][a.col].ocupacion - 1)
            break 
            
        estado_turno = {
            'mapa': [[celda.estado for celda in fila] for fila in mapa_actual.matriz],
            'agentes': [{'id': a.id, 'f': a.fila, 'c': a.col, 'estado': a.estado} for a in agentes]
        }
        historial_simulacion.append(estado_turno)
        
        for agente in agentes:
            if agente.estado == 'vivo':
                if not agente.ruta_planeada:
                    agente.replanificar(mapa_actual)
                elif agente.ruta_planeada:
                    sig_paso = agente.ruta_planeada[0]
                    movs = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1), 4: (0, 0)}
                    df, dc = movs[sig_paso]
                    if mapa_actual.matriz[agente.fila + df][agente.col + dc].estado == 'f':
                        agente.replanificar(mapa_actual)
                agente.mover(mapa_actual)
                         
        if turno_actual % k_turnos_fuego == 0:
            mapa_actual.propagar_fuego()
            for agente in agentes:
                if agente.estado == 'vivo' and mapa_actual.matriz[agente.fila][agente.col].estado == 'f':
                    agente.estado = 'muerto'
                    mapa_actual.matriz[agente.fila][agente.col].ocupacion = max(0, mapa_actual.matriz[agente.fila][agente.col].ocupacion - 1)
        
        turno_actual += 1
          
    estado_final = {
        'mapa': [[celda.estado for celda in fila] for fila in mapa_actual.matriz],
        'agentes': [{'id': a.id, 'f': a.fila, 'c': a.col, 'estado': a.estado} for a in agentes]
    }
    historial_simulacion.append(estado_final)

    vivos = sum(1 for a in agentes if a.estado == 'vivo')
    escapados = sum(1 for a in agentes if a.estado == 'escapo')
    muertos = sum(1 for a in agentes if a.estado == 'muerto')
    print(f"\nAgentes vivos: {vivos} | Escaparon: {escapados} | Bajas: {muertos}")
          
    print("\n[+] SIMULACION FINALIZADA.")
    tasa_supervivencia = (escapados / len(agentes)) * 100
    print(f"Tasa de Supervivencia: {tasa_supervivencia:.2f}%")
    
    return historial_simulacion

