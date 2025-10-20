import pygame
import random
pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Atrapa monedas")
clock = pygame.time.Clock()

# Jugador(rectangulo)
jugador = pygame.Rect(ANCHO//2 - 25, ALTO//2 - 25, 50, 50)
VEL = 6

# Monedas y agregue bombas
MONEDA_RADIO = 12
monedas = []
bombas = []
SPAWN_MS = 900
ULTIMO_SPAWN = 0
MAX_MONEDAS = 8

# HUD
fuente = pygame.font.Font(None, 32)
puntos = 0
TIEMPO_TOTAL_MS = 30_000 # 30 segundos
inicio_ms = pygame.time.get_ticks()

running = True
while running:
    dt = clock.tick(60) # ms transcurridos desde el frame
    ahora = pygame.time.get_ticks()

    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            running = False
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
    # Movimiento
    teclas = pygame.key.get_pressed()
    dx = (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) - (teclas[pygame.K_LEFT] or teclas[pygame.K_a])
    dy = (teclas[pygame.K_DOWN] or teclas[pygame.K_s]) - (teclas[pygame.K_UP] or teclas[pygame.K_w])
    jugador.x += int(dx * VEL)
    jugador.y += int(dy * VEL)
    
    # Limitar a la pantalla
    jugador.clamp_ip(pygame.Rect(0, 0, ANCHO, ALTO))

    # Aumentar dificultad: reducir SPAWN_MS con el tiempo
    dificultad = 1 + (ahora - inicio_ms) / TIEMPO_TOTAL_MS
    spawn_interval = max(300, int(SPAWN_MS / dificultad))

    # Spawnear monedas y bombas
    if ahora - ULTIMO_SPAWN >= spawn_interval and len(monedas) < MAX_MONEDAS:
        x = random.randint(MONEDA_RADIO, ANCHO - MONEDA_RADIO)
        y = random.randint(MONEDA_RADIO, ALTO - MONEDA_RADIO)
        rect = pygame.Rect(x - MONEDA_RADIO, y - MONEDA_RADIO, MONEDA_RADIO*2, MONEDA_RADIO*2)
        if random.random() < 0.15:
            bombas.append(rect)
        else:
            monedas.append((rect, random.choice([1, 2])))  # valor 1 o 2
        ULTIMO_SPAWN = ahora

    # Colisiones con monedas
    recogidas = []
    for i, (m, valor) in enumerate(monedas):
        if jugador.colliderect(m):
            puntos += valor
            recogidas.append(i)
    for i in reversed(recogidas):
        monedas.pop(i)

    # Colisiones con bombas
    bombas_recogidas = []
    for i, b in enumerate(bombas):
        if jugador.colliderect(b):
            TIEMPO_TOTAL_MS -= 3000  # restar 3 segundos
            bombas_recogidas.append(i)
    for i in reversed(bombas_recogidas):
        bombas.pop(i)

    # Tiempo restante
    transcurrido = ahora - inicio_ms
    restante_ms = max(0, TIEMPO_TOTAL_MS - transcurrido)
    if restante_ms == 0:
        game_over_txt = pygame.font.Font(None, 64).render("¡Tiempo!", True, (255, 220, 60))
        puntaje_txt = pygame.font.Font(None, 48).render(f"Puntaje: {puntos}", True, (255, 255, 255))
        pantalla.blit(game_over_txt, game_over_txt.get_rect(center=(ANCHO//2, ALTO//2 - 30)))
        pantalla.blit(puntaje_txt, puntaje_txt.get_rect(center=(ANCHO//2, ALTO//2 + 30)))
        pygame.display.flip()
        pygame.time.delay(1500)
        running = False
        continue

    # Dibujo
    pantalla.fill((12, 26, 38))
    for m, valor in monedas:
        color = (255, 215, 0) if valor == 1 else (255, 100, 0)
        pygame.draw.circle(pantalla, color, m.center, MONEDA_RADIO)
    for b in bombas:
        pygame.draw.circle(pantalla, (200, 0, 0), b.center, MONEDA_RADIO)
    pygame.draw.rect(pantalla, (80, 200, 255), jugador, border_radius=6)

    # HUD
    seg = restante_ms // 1000
    hud1 = fuente.render(f"Puntos: {puntos}", True, (255, 255, 255))
    hud2 = fuente.render(f"Tiempo: {seg:02d}s", True, (255, 255, 255))
    pantalla.blit(hud1, (10, 10))
    pantalla.blit(hud2, (10, 40))

    pygame.display.flip()

pygame.quit()
