# visualizador.py
try:
    import pygame
except ImportError:
    print("[!] Error: Pygame no está instalado. Ejecuta 'pip install pygame' en tu consola.")
    pygame = None

def reproducir(historial, ancho_celda=40):
    if not pygame or not historial:
        return

    # Configuraciones iniciales basadas en el tamaño del mapa
    filas = len(historial[0]['mapa'])
    columnas = len(historial[0]['mapa'][0])
    
    ANCHO = columnas * ancho_celda
    ALTO = filas * ancho_celda

    pygame.display.init() # Solo iniciamos el motor gráfico 
    pygame.font.init()    # Y el motor de texto
    
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Simulador de Evacuación - Reproductor")
    reloj = pygame.time.Clock()
    
    # Fuente en negrita para que los números resalten sobre el círculo
    fuente_agentes = pygame.font.SysFont("Arial", 18, bold=True)

    # Definición de Colores (RGB)
    BLANCO = (240, 240, 240)
    NEGRO = (40, 40, 40)
    ROJO_FUEGO = (220, 50, 50)
    VERDE_SALIDA = (50, 200, 50)
    AZUL_AGENTE = (50, 100, 250)
    GRIS_INICIO = (180, 180, 180)
    CRUZ_MUERTE = (150, 0, 0)
    BLANCO_TEXTO = (255, 255, 255)
    
    turno_actual = 0
    total_turnos = len(historial)
    pausado = False
    
    print("\n[Pygame] Reproductor iniciado.")
    print("Controles: [ESPACIO] Pausa/Play | [FLECHA DER] Avanzar paso | [FLECHA IZQ] Retroceder paso")
    
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausado = not pausado
                elif evento.key == pygame.K_RIGHT:
                    if pausado and turno_actual < total_turnos - 1:
                        turno_actual += 1
                elif evento.key == pygame.K_LEFT:
                    if pausado and turno_actual > 0:
                        turno_actual -= 1

        pantalla.fill(BLANCO)
        
        # Extraemos la "foto" del turno actual
        estado = historial[turno_actual]
        mapa = estado['mapa']
        agentes = estado['agentes']

        # 1. Dibujar la grilla y el mapa
        for f in range(filas):
            for c in range(columnas):
                celda = mapa[f][c]
                color = BLANCO
                if celda == 'm':
                    color = NEGRO
                elif celda == 'f':
                    color = ROJO_FUEGO
                elif celda == 'g':
                    color = VERDE_SALIDA
                elif celda == 's':
                    color = GRIS_INICIO
                    
                rectangulo = (c * ancho_celda, f * ancho_celda, ancho_celda, ancho_celda)
                pygame.draw.rect(pantalla, color, rectangulo)
                pygame.draw.rect(pantalla, (200, 200, 200), rectangulo, 1) 

        # 2. Agrupar a los agentes por posición para saber cuántos hay en cada celda
        posiciones_vivos = {}
        posiciones_muertos = set()
        
        for agente in agentes:
            pos = (agente['f'], agente['c'])
            if agente['estado'] == 'vivo':
                # Sumamos 1 a la cantidad de agentes en esa posición
                posiciones_vivos[pos] = posiciones_vivos.get(pos, 0) + 1
            elif agente['estado'] == 'muerto':
                posiciones_muertos.add(pos)

        # 3. Dibujar a los agentes muertos
        for f, c in posiciones_muertos:
            x = c * ancho_celda
            y = f * ancho_celda
            pygame.draw.line(pantalla, CRUZ_MUERTE, (x + 8, y + 8), (x + ancho_celda - 8, y + ancho_celda - 8), 4)
            pygame.draw.line(pantalla, CRUZ_MUERTE, (x + ancho_celda - 8, y + 8), (x + 8, y + ancho_celda - 8), 4)

        # 4. Dibujar a los agentes vivos y su contador
        for (f, c), cantidad in posiciones_vivos.items():
            centro = (c * ancho_celda + ancho_celda // 2, f * ancho_celda + ancho_celda // 2)
            radio = ancho_celda // 3
            pygame.draw.circle(pantalla, AZUL_AGENTE, centro, radio)
            
            # ¡La magia ocurre aquí! Si hay más de un agente, dibujamos el número encima
            if cantidad > 1:
                texto = fuente_agentes.render(str(cantidad), True, BLANCO_TEXTO)
                rect_texto = texto.get_rect(center=centro)
                pantalla.blit(texto, rect_texto)

        # Actualizar el título con el turno actual
        pygame.display.set_caption(f"Evacuación | Turno {turno_actual} de {total_turnos - 1} | {'PAUSADO' if pausado else 'PLAY'}")
        
        pygame.display.flip()

        # Control de avance de frames
        if not pausado:
            if turno_actual < total_turnos - 1:
                turno_actual += 1
                reloj.tick(5) 
            else:
                pausado = True 
        else:
            reloj.tick(15) 

    
    pygame.display.quit() 
   
    pygame.quit()