# ui.py
from __future__ import annotations
import pygame

class Button:
    def __init__(self, rect: pygame.Rect, text: str, font: pygame.font.Font, fg=(255, 255, 255), bg=(60, 60, 60), bg_hover=(90, 90, 90)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.fg = fg
        self.bg = bg
        self.bg_hover = bg_hover
        self.hover = False
        self._render_cache = None

    def draw(self, surf: pygame.Surface):
        color = self.bg_hover if self.hover else self.bg

        pygame.draw.rect(surf, color, self.rect, border_radius=10)
        if not self._render_cache:
            self._render_cache = self.font.render(self.text, True, self.fg)

        text_surf = self._render_cache
        text_rect = text_surf.get_rect(center=self.rect.center)
        surf.blit(text_surf, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False