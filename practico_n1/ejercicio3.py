import pygame
import random
pygame.init()

ANCHO, ALTO = 640, 480
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pelota que rebota")
clock = pygame.time.Clock()

x, y = ANCHO // 2, ALTO // 2
radio = 20
dx, dy = 4, 3
color = (0, 200, 120)
rebotes = 0
font = pygame.font.Font(None, 36)
vel_max = 12

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    x += dx
    y += dy

    # Rebotar en bordes, cambio de color y cuenta los rebotes mas el aumento de velocidad vada ver que rebota la pelota
    if x - radio <= 0 or x + radio >= ANCHO:
        dx = -dx
        rebotes += 1
        color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        dx *= 1.05
        dx = max(min(dx, vel_max), -vel_max)
    if y - radio <= 0 or y + radio >= ALTO:
        dy = -dy
        rebotes += 1
        color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        dy *= 1.05
        dy = max(min(dy, vel_max), -vel_max)

    pantalla.fill((0, 0, 0))
    pygame.draw.circle(pantalla, color, (int(x), int(y)), radio)

    texto = font.render(f"Rebotes: {rebotes}", True, (255, 255, 255))
    pantalla.blit(texto, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
