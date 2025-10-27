# Mi Juego Pygame

Un juego desarrollado con Pygame que incluye sistema de puntuaciones, base de datos SQLite.

## Estructura del Proyecto

```
mi_juego/
├─ main.py              # Loop principal de Pygame
├─ db.py                # Capa de datos SQLite
├─ paths.py             # Utilidades de rutas para PyInstaller
├─ ui.py                # Componentes de interfaz
├─ scene/               # Escenas del juego
│  ├─ start_menu.py
│  ├─ game_scene.py
│  └─ leaderboard_scene.py
├─ res/                 # Assets del juego
│  ├─ img/              # Imágenes
│  ├─ sfx/              # Efectos de sonido
│  └─ fonts/            # Fuentes
├─ data/                # Base de datos inicial (opcional)
│  └─ game_base.db
├─ icons/               # Iconos para el ejecutable
│  ├─ app.ico           # Windows
│  └─ app.icns          # macOS
├─ requirements.txt     # Dependencias
└─ README.md           # Este archivo
```

## Instalación y Configuración

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar en modo desarrollo

```bash
python main.py
```

## Empaquetado con PyInstaller

### Comando básico (one-directory)

```bash
pyinstaller --name "MiJuego" --windowed --icon icons/app.ico --add-data "res;res" --add-data "data;data" main.py
```

### Modo onefile (un solo ejecutable)

```bash
pyinstaller --onefile --name "MiJuego" --windowed --icon icons/app.ico --add-data "res;res" --add-data "data;data" main.py
```

**Nota:** En Windows usa `;` como separador en `--add-data`. En macOS/Linux usa `:`.

### Parámetros explicados

- `--windowed`: Evita mostrar la consola (usa `--console` para debug)
- `--icon`: Especifica el icono del ejecutable
- `--add-data`: Incluye carpetas de recursos en el ejecutable
- `--onefile`: Crea un solo archivo ejecutable (más lento al iniciar)

## Ubicación de la Base de Datos

La base de datos se crea automáticamente en la carpeta de datos del usuario:

- **Windows**: `C:\Users\<usuario>\AppData\Local\MiJuegoPygame\game.db`
- **macOS**: `/Users/<usuario>/Library/Application Support/MiJuegoPygame/game.db`
- **Linux**: `/home/<usuario>/.local/share/MiJuegoPygame/game.db`

## Características

- ✅ Sistema de puntuaciones persistente
- ✅ Base de datos SQLite con esquema versionado
- ✅ Empaquetado multiplataforma con PyInstaller
- ✅ Gestión automática de rutas de recursos
- ✅ Estructura de proyecto profesional

## Desarrollo

### Agregar nuevos assets

1. Coloca imágenes en `res/img/`
2. Coloca sonidos en `res/sfx/`
3. Coloca fuentes en `res/fonts/`
4. Usa `resource_path()` para cargar recursos:

```python
from paths import resource_path
import pygame

# Cargar imagen
img = pygame.image.load(resource_path('res', 'img', 'player.png'))

# Cargar fuente
font = pygame.font.Font(str(resource_path('res', 'fonts', 'PressStart2P.ttf')), 24)
```

### Migración de base de datos

Para actualizar el esquema de la base de datos:

1. Incrementa `PRAGMA user_version` en `db.py`
2. Implementa función de migración
3. Llama la migración después de conectar

## Solución de Problemas

### El ejecutable no encuentra assets
- Verifica que usas `resource_path()` para cargar recursos
- Revisa los separadores en `--add-data` (Windows: `;`, macOS/Linux: `:`)

### Error "database is locked"
- Usa una sola conexión por proceso
- No abras/cierres la DB en cada frame

### Antivirus bloquea el ejecutable
- Usa un instalador reconocido
- Agrega exclusión temporal para pruebas

## Licencia

Este proyecto es parte de las prácticas de Software Factory.
