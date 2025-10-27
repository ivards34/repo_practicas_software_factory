# main.py
import sys
import pygame
from paths import db_path, resource_path, user_data_dir
import shutil

WIDTH, HEIGHT = 800, 450
FPS = 60

def ensure_database():
    """Primera ejecución: si no hay DB, crea/copia"""
    target = db_path()
    if not target.exists():
        base_candidate = resource_path('data', 'game_base.db')
        user_data_dir()  # asegura carpeta
        if base_candidate.exists():
            shutil.copy2(base_candidate, target)
        else:
            import db
            conn = db.connect()
            db.init_db(conn)
            conn.close()

def boot():
    """Inicialización del juego"""
    # asegurar carpeta de datos y DB
    user_data_dir()
    if not db_path().exists():
        conn = db.connect()
        db.init_db(conn)
        conn.close()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mi Juego — Demo")
    clock = pygame.time.Clock()

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Dibujar pantalla básica
        screen.fill((25, 25, 28))
        
        # Mostrar texto básico
        font = pygame.font.Font(None, 36)
        text = font.render("Mi Juego Pygame", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, text_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    boot()
    main()