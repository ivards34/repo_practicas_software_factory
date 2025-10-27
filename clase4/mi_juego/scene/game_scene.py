# scenes/game_scene.py
import pygame
import db

class GameScene:
    def __init__(self, manager):
        self.m = manager
        self.font = None
        self.state = 'ask_name'  # ask_name -> play
        self.name = ''
        self.score = 0
        self.level = 1
        self.conn = None

    def on_enter(self):
        self.font = pygame.font.SysFont(None, 30)
        self.conn = db.connect(); db.init_db(self.conn)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == 'ask_name':
                if event.key == pygame.K_RETURN and self.name.strip():
                    self.state = 'play'
                elif event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]
                else:
                    ch = event.unicode
                    if ch and ch.isprintable() and len(self.name) < 20:
                        self.name += ch
            elif self.state == 'play':
                if event.key == pygame.K_ESCAPE:
                    self.finish_game()
                elif event.key == pygame.K_SPACE:
                    self.score += 10
                elif event.key == pygame.K_RIGHT:
                    self.score += 1
                elif event.key == pygame.K_LEFT and self.score > 0:
                    self.score -= 1


    def update(self, dt):
        if self.state == 'play':
            # suma pasiva
            self.score += int(4 * dt)

    def draw(self, screen):
        if self.state == 'ask_name':
            t1 = self.font.render("Ingresa tu nombre y presiona ENTER:", True, (240,240,240))
            t2 = self.font.render(self.name + '|', True, (180,255,180))
            screen.blit(t1, (40, 120))
            screen.blit(t2, (40, 160))
        else:
            t1 = self.font.render(f"Jugador: {self.name} Nivel: {self.level}", True, (240,240,240))
            t2 = self.font.render(f"Puntaje: {self.score} [ESPACIO +10, → +1, ← -1, ESC termina]", True, (240,240,240))
            screen.blit(t1, (20, 20))
            screen.blit(t2, (20, 60))

    def finish_game(self):
        try:
            pid = db.get_or_create_jugador(self.conn, self.name.strip())
            db.registrar_puntuacion(self.conn, pid, int(self.score), int(self.level))
        finally:
            try:
                self.conn.close()
            except Exception:
                pass
        # ir a ranking con última puntuación
        from .leaderboard_scene import LeaderboardScene
        self.m.set_scene(LeaderboardScene(self.m, after_game=True, last_score=int(self.score)))