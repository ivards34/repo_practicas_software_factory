# paths.py
from pathlib import Path
import os

def user_data_dir():
    """Crea y retorna el directorio de datos del usuario"""
    if os.name == 'nt':  # Windows
        base = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming'))
    elif os.name == 'posix':  # macOS/Linux
        base = Path.home() / '.local' / 'share'
    else:
        base = Path.home()
    
    app_dir = base / 'mi_juego'
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir

def db_path():
    """Retorna la ruta completa del archivo de base de datos"""
    return user_data_dir() / 'jugadores.db'
