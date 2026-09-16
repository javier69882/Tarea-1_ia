def ejecutar_simulacion(mapa_actual, ClaseAgente, nombre_simulacion="Simulación"):
    print(f"\n[*] Iniciando Dinámica con Agentes ({nombre_simulacion})...")
    
    # Instanciamos a los agentes dinámicamente según la clase que se pase
    agentes, meta = ClaseAgente.spawnear_desde_mapa(mapa_actual)
    
    if not agentes or not meta:
        print("[!] Error: No se encontró inicio ('s') o meta ('g') en el mapa.")
        return None
                 
    k_turnos_fuego = 2 
    turno_actual = 1
    historial_simulacion = []
    
    while any(a.estado == 'vivo' for a in agentes):
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