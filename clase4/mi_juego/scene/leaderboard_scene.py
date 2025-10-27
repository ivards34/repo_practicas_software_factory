# scenes/leaderboard_scene.py
import pygame
import db
from ui import Button

class LeaderboardScene:
    def __init__(self, manager, after_game: bool, last_score: int = None):
        self.m = manager
        self.after_game = after_game
        self.last_score = last_score
        self.font_title = None
        self.font_row = None
        self.font_info = None
        self.btn_play_again = None
        self.btn_menu = None
        self.btn_quit = None
        self.conn = None
        self.rows = []

    def on_enter(self):
        self.font_title = pygame.font.SysFont(None, 48)
        self.font_row = pygame.font.SysFont(None, 28)
        self.font_info = pygame.font.SysFont(None, 24)
        w, h = self.m.screen.get_size()
        bw, bh = 260, 50
        cx = w // 2
        y0 = 280
        sep = 60
        self.btn_play_again = Button(pygame.Rect(cx - bw//2, y0, bw, bh), "Volver a jugar", self.font_row)
        self.btn_menu = Button(pygame.Rect(cx - bw//2, y0 + sep, bw, bh), "Volver al menú", self.font_row)
        self.btn_quit = Button(pygame.Rect(cx - bw//2, y0 + 2*sep, bw, bh), "Salir", self.font_row)
        self.conn = db.connect()
        db.init_db(self.conn)
        self.rows = db.top_n(self.conn, 10)

    def handle_event(self, event):
        if self.btn_play_again.handle_event(event):
            from .game_scene import GameScene
            self.m.set_scene(GameScene(self.m))
        elif self.btn_menu.handle_event(event):
            from .start_menu import StartMenu
            self.m.set_scene(StartMenu(self.m))
        elif self.btn_quit.handle_event(event):
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def draw(self, screen):
        w, _ = screen.get_size()
        title = self.font_title.render("Top 10 Puntajes", True, (240, 230, 70))
        screen.blit(title, title.get_rect(center=(w//2, 60)))

        y = 110
        for idx, r in enumerate(self.rows, start=1):
            line = f"{idx:>2}. {r['nombre']:<12} {r['puntaje']:>5} (Nivel {r['nivel']})"
            t = self.font_row.render(line, True, (235,235,235))
            screen.blit(t, (160, y))
            y += 28

        if self.after_game and self.last_score is not None:
            info = self.font_info.render(f"Tu último puntaje: {self.last_score}", True, (180, 220, 255))
            screen.blit(info, info.get_rect(center=(w//2, 250)))

        for b in (self.btn_play_again, self.btn_menu, self.btn_quit):
            b.draw(screen)

    def __del__(self):
        try:
            if self.conn:
                self.conn.close()
        except Exception:
            pass