# main.py
import sys
import pygame
from scene.start_menu import StartMenu
from paths import user_data_dir, db_path

WIDTH, HEIGHT = 800, 450
FPS = 60

class SceneManager:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.scene = None

    def set_scene(self, scene):
        self.scene = scene
        if hasattr(self.scene, 'on_enter'):
            self.scene.on_enter()

    def handle_event(self, event):
        if self.scene and hasattr(self.scene, 'handle_event'):
            self.scene.handle_event(event)

    def update(self, dt):
        if self.scene and hasattr(self.scene, 'update'):
            self.scene.update(dt)

    def draw(self):
        if self.scene and hasattr(self.scene, 'draw'):
            self.scene.draw(self.screen)

def boot():


    user_data_dir()
    if not db_path().exists():
# crear base vacía
        import db
        conn = db.connect(); db.init_db(conn); conn.close()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mi Juego — Demo Flujo")
    clock = pygame.time.Clock()

    manager = SceneManager(screen)
    manager.set_scene(StartMenu(manager))

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                manager.handle_event(event)

        manager.update(dt)
        screen.fill((25, 25, 28))
        manager.draw()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    boot()
    main()