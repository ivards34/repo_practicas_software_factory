import pygame
import random
pygame.init()

ANCHO, ALTO = 900, 540
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Tiro al blanco")
clock = pygame.time.Clock()

fuente = pygame.font.Font(None, 32)
grande = pygame.font.Font(None, 64)
pygame.mouse.set_visible(False)

# Cooldown visual
cooldown_timer = 0
COOLDOWN_MS = 150

class Diana:
    def __init__(self, tipo="horizontal"):
        self.radio = random.randint(16, 28)
        self.valor = 2 if self.radio < 20 else 1
        self.x = random.randint(self.radio + 40, ANCHO - self.radio - 40)
        self.y = random.randint(100, ALTO - 100)
        self.vel = random.choice([3, 4, 5])
        self.dir = random.choice([-1, 1])
        self.tipo = tipo
        self.color = (220, 60, 90)

    def update(self):
        if self.tipo == "horizontal":
            self.x += self.dir * self.vel
            if self.x - self.radio <= 40 or self.x + self.radio >= ANCHO - 40:
                self.dir *= -1
        elif self.tipo == "vertical":
            self.y += self.dir * self.vel
            if self.y - self.radio <= 40 or self.y + self.radio >= ALTO - 40:
                self.dir *= -1
        elif self.tipo == "diagonal":
            self.x += self.dir * self.vel
            self.y += self.dir * self.vel
            if self.x - self.radio <= 40 or self.x + self.radio >= ANCHO - 40:
                self.dir *= -1
            if self.y - self.radio <= 40 or self.y + self.radio >= ALTO - 40:
                self.dir *= -1

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (self.x, self.y), self.radio)
        pygame.draw.circle(surf, (255, 255, 255), (self.x, self.y), max(4, self.radio//2), width=2)

    def colisiona(self, pos):
        mx, my = pos
        dx = mx - self.x
        dy = my - self.y
        return dx*dx + dy*dy <= self.radio*self.radio

# Crear dianas mixtas
tipos = ["horizontal", "vertical", "diagonal"]
dianas = [Diana(random.choice(tipos)) for _ in range(6)]

# Stats
aciertos = 0
intentos = 0
modo_practica = True  # ← cambiar a False para modo con tiempo
tiempo_ms = 40_000
inicio_ms = pygame.time.get_ticks()

running = True
while running:
    dt = clock.tick(60)
    ahora = pygame.time.get_ticks()
    cooldown_timer = max(0, cooldown_timer - dt)

    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            running = False
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            intentos += 1
            pos = pygame.mouse.get_pos()
            cooldown_timer = COOLDOWN_MS
            for i, d in enumerate(dianas):
                if d.colisiona(pos):
                    aciertos += d.valor
                    dianas[i] = Diana(random.choice(tipos))
                    break

    restante = max(0, tiempo_ms - (ahora - inicio_ms))
    if not modo_practica and restante == 0:
        acc = (aciertos / intentos * 100) if intentos > 0 else 0.0
        pantalla.fill((20, 20, 20))
        fin = grande.render("¡Tiempo!", True, (255, 220, 60))
        res = fuente.render(f"Aciertos: {aciertos} Intentos: {intentos} Precisión: {acc:.1f}%", True, (255, 255, 255))
        pantalla.blit(fin, fin.get_rect(center=(ANCHO//2, ALTO//2 - 24)))
        pantalla.blit(res, res.get_rect(center=(ANCHO//2, ALTO//2 + 24)))
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False
        continue

    for d in dianas:
        d.update()

    pantalla.fill((15, 28, 40))
    pygame.draw.rect(pantalla, (30, 45, 60), (0, 0, 40, ALTO))
    pygame.draw.rect(pantalla, (30, 45, 60), (ANCHO-40, 0, 40, ALTO))
    for d in dianas:
        d.draw(pantalla)

    acc = (aciertos / intentos * 100) if intentos > 0 else 0.0
    seg = restante // 1000
    hud1 = fuente.render(f"Aciertos: {aciertos}", True, (255, 255, 255))
    hud2 = fuente.render(f"Intentos: {intentos}", True, (255, 255, 255))
    hud3 = fuente.render(f"Precisión: {acc:.1f}%", True, (255, 255, 255))
    hud4 = fuente.render(f"Tiempo: {seg:02d}s", True, (255, 255, 255)) if not modo_practica else fuente.render("Modo práctica", True, (255, 255, 255))
    pantalla.blit(hud1, (10, 8))
    pantalla.blit(hud2, (10, 34))
    pantalla.blit(hud3, (10, 60))
    pantalla.blit(hud4, (10, 86))

    mx, my = pygame.mouse.get_pos()
    pygame.draw.circle(pantalla, (255, 255, 255), (mx, my), 12, width=2)
    pygame.draw.line(pantalla, (255, 255, 255), (mx-18, my), (mx-4, my), width=2)
    pygame.draw.line(pantalla, (255, 255, 255), (mx+4, my), (mx+18, my), width=2)
    pygame.draw.line(pantalla, (255, 255, 255), (mx, my-18), (mx, my-4), width=2)
    pygame.draw.line(pantalla, (255, 255, 255), (mx, my+4), (mx, my+18), width=2)

    if cooldown_timer > 0:
        pygame.draw.circle(pantalla, (255, 0, 0), (mx, my), 20, width=2)

    pygame.display.flip()

pygame.quit()
