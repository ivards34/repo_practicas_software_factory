import pygame

pygame.init()
ANCHO, ALTO = 640, 480
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Hola Pygame")

fuente = pygame.font.Font(None, 48)
texto_principal = fuente.render("¡Bienvenido a Pygame!", True, (255, 255, 255))
texto_nombre = fuente.render("Ivar", True, (255, 255, 255))

rect_texto_principal = texto_principal.get_rect(center=(ANCHO // 2, ALTO // 2 - 30))
rect_texto_nombre = texto_nombre.get_rect(center=(ANCHO // 2, ALTO // 2 + 30))

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT:
                rect_texto_principal.x -= 10
                
            elif event.key == pygame.K_RIGHT:
                rect_texto_principal.x += 10
               
            elif event.key == pygame.K_UP:
                rect_texto_principal.y -= 10
                
            elif event.key == pygame.K_DOWN:
                rect_texto_principal.y += 10
                

    pantalla.fill((100, 180, 100))  # Fondo verde suave
    pantalla.blit(texto_principal, rect_texto_principal)
    pantalla.blit(texto_nombre, rect_texto_nombre)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
