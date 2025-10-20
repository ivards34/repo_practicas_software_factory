import pygame
pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mover con flechas")
clock = pygame.time.Clock()

jugador = pygame.Rect(100, 100, 60, 60)  # x, y, ancho, alto
vel_base = 300  # píxeles por segundo

running = True
while running:
    dt = clock.tick(60) / 1000.0  # segundos por frame

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    teclas = pygame.key.get_pressed()

    # Sprint con Shift
    if teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT]:
        vel_actual = vel_base * 2
    else:
        vel_actual = vel_base

    # Movimiento con dt
    if teclas[pygame.K_LEFT]:
        jugador.x -= int(vel_actual * dt)
    if teclas[pygame.K_RIGHT]:
        jugador.x += int(vel_actual * dt)
    if teclas[pygame.K_UP]:
        jugador.y -= int(vel_actual * dt)
    if teclas[pygame.K_DOWN]:
        jugador.y += int(vel_actual * dt)

    # Limitar dentro de la ventana
    jugador.clamp_ip(pantalla.get_rect())

    pantalla.fill((25, 25, 25))
    pygame.draw.rect(pantalla, (220, 70, 70), jugador)
    pygame.display.flip()

pygame.quit()
