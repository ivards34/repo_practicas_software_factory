# scenes/start_menu.py
import pygame
from ui import Button

class StartMenu:
    def __init__(self, manager):
        self.m = manager
        self.font_title = None
        self.font_btn = None
        self.btn_play = None
        self.btn_rank = None
        self.btn_quit = None

    def on_enter(self):
        self.font_title = pygame.font.SysFont(None, 56)
        self.font_btn = pygame.font.SysFont(None, 36)
        w, h = self.m.screen.get_size()
        bw, bh = 260, 50
        cx = w // 2; y0 = 180; sep = 70
        self.btn_play = Button(pygame.Rect(cx - bw//2, y0, bw, bh), "Jugar", self.font_btn)
        self.btn_rank = Button(pygame.Rect(cx - bw//2, y0 + sep, bw, bh), "Ver Ranking", self.font_btn)
        self.btn_quit = Button(pygame.Rect(cx - bw//2, y0 + 2*sep, bw, bh), "Salir", self.font_btn)

    def handle_event(self, event):
        if self.btn_play.handle_event(event):
            from .game_scene import GameScene
            self.m.set_scene(GameScene(self.m))
        elif self.btn_rank.handle_event(event):
            from .leaderboard_scene import LeaderboardScene
            self.m.set_scene(LeaderboardScene(self.m, after_game=False, last_score=None))
        elif self.btn_quit.handle_event(event):
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def update(self, dt):
        pass

    def draw(self, screen):

        w, _ = screen.get_size()
        title = self.font_title.render("Mi Juego — Pantalla de Inicio", True, (230, 230, 240))
        screen.blit(title, title.get_rect(center=(w//2, 100)))
        for b in (self.btn_play, self.btn_rank, self.btn_quit):
            b.draw(screen)