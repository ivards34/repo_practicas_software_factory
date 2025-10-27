# paths.py
from __future__ import annotations
import os, sys
from pathlib import Path

APP_NAME = "MiJuegoPygame"

# Detecta si corre empaquetado con PyInstaller
IS_FROZEN = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

# Ruta a recursos empaquetados (solo lectura)
def resource_path(*parts: str) -> Path:
    """Devuelve la ruta a un recurso (assets) tanto en dev como en ejecutable."""
    if IS_FROZEN:
        base = Path(sys._MEIPASS)  # type: ignore[attr-defined]
    else:
        base = Path(__file__).parent
    return base.joinpath(*parts)

# Ruta de datos del usuario (lectura/escritura)
def user_data_dir() -> Path:
    try:
        from appdirs import user_data_dir as _udd
        p = Path(_udd(APP_NAME, APP_NAME))
    except Exception:
        # Fallback simple si no está appdirs
        if sys.platform.startswith('win'):
            base = Path(os.getenv('LOCALAPPDATA', Path.home() / 'AppData' / 'Local'))
        elif sys.platform == 'darwin':
            base = Path.home() / 'Library' / 'Application Support'
        else:
            base = Path(os.getenv('XDG_DATA_HOME', Path.home() / '.local' / 'share'))
        p = base / APP_NAME
    p.mkdir(parents=True, exist_ok=True)
    return p

# Ruta al archivo de base de datos real (escribible)
def db_path() -> Path:
    return user_data_dir() / 'game.db'
