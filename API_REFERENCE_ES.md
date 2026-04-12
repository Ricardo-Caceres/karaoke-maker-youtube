# 📚 Referencia de API

Documentación completa de la API para la Suite de Procesamiento de Audio y Video de YouTube DL.

## 📋 Tabla de Contenidos

- [Visión General](#visión-general)
- [Módulo: app.py](#módulo-apppy)
- [Módulo: karaoke_generator.py](#módulo-karaoke_generatorpy)
- [Módulo: movies.py](#módulo-moviespy)
- [Manejo de Errores](#manejo-de-errores)
- [Clases de Configuración](#clases-de-configuración)
- [Funciones Utilitarias](#funciones-utilitarias)
- [Ejemplos](#ejemplos)

## 🎯 Visión General

Esta referencia de API proporciona documentación detallada para todas las funciones, clases y métodos públicos en la suite de YouTube DL. Cada módulo está diseñado para ser tanto independiente como integrable con otros componentes.

### Estructura de Importación
```python
# Importaciones de módulos individuales
from app import convert_to_audio, separate_voice
from movies import download_movie
from karaoke_generator import (
    download_audio, 
    separate_vocals, 
    generate_timed_lyrics, 
    create_karaoke_video
)
```

### Tipos Comunes
```python
from typing import Dict, List, Tuple, Optional, Union
from pathlib import Path

# Alias de tipos
URLString = str
FilePath = Union[str, Path]
AudioFormat = str  # 'mp3', 'wav', 'flac'
VideoFormat = str  # 'mp4', 'mkv', 'avi'
```

---

## 🎵 Módulo: app.py

Módulo de procesamiento de audio para conversión de videos de YouTube y separación de voz.

### Funciones

#### `convert_to_audio(url: str) -> str`

Convierte un video de YouTube a archivo de audio de alta calidad.

**Parámetros:**
- `url` (str): URL del video de YouTube

**Retorna:**
- `str`: Ruta al archivo de audio descargado

**Lanza:**
- `yt_dlp.DownloadError`: Si la descarga del video falla
- `OSError`: Si las operaciones del sistema de archivos fallan
- `ValueError`: Si la URL es inválida

**Ejemplo:**
```python
from app import convert_to_audio

try:
    audio_path = convert_to_audio("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    print(f"Audio guardado en: {audio_path}")
except Exception as e:
    print(f"Error: {e}")
```

**Configuración:**
```python
# Configuración interna (modificar en el código fuente)
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',      # Formato: mp3, wav, flac
        'preferredquality': '192',    # Calidad: 96, 128, 192, 320
    }],
    'outtmpl': 'downloads/%(title)s.%(ext)s'
}
```

#### `separate_voice(audio_file: str) -> None`

Separa voces de la música de fondo usando separación harmónico-percusiva.

**Parámetros:**
- `audio_file` (str): Ruta al archivo de audio de entrada

**Retorna:**
- `None`: Los archivos se guardan en el directorio downloads/

**Efectos Secundarios:**
- Crea `downloads/voice.wav` - voces aisladas
- Crea `downloads/background.wav` - música de fondo

**Lanza:**
- `librosa.LibrosaError`: Si la carga/procesamiento de audio falla
- `soundfile.LibsndfileError`: Si el guardado de audio falla
- `FileNotFoundError`: Si el archivo de entrada no existe

**Ejemplo:**
```python
from app import separate_voice

try:
    separate_voice("downloads/cancion.mp3")
    print("✅ Separación de voz completa")
    print("📁 Revisa downloads/voice.wav y downloads/background.wav")
except FileNotFoundError:
    print("❌ Archivo de audio no encontrado")
```

**Detalles Técnicos:**
- **Algoritmo**: Separación de Fuentes Harmónico-Percusiva (HPSS)
- **Calidad**: Buena para música con separación clara entre voces e instrumentos
- **Limitaciones**: Puede no funcionar bien con música muy procesada o sintetizada

#### `download_audio(audio_file: str) -> bytes`

Lee el contenido del archivo de audio en memoria.

**Parámetros:**
- `audio_file` (str): Ruta al archivo de audio

**Retorna:**
- `bytes`: Contenido crudo del archivo de audio

**Lanza:**
- `FileNotFoundError`: Si el archivo no existe
- `PermissionError`: Si el archivo no se puede leer

**Ejemplo:**
```python
from app import download_audio

audio_data = download_audio("downloads/cancion.mp3")
print(f"Tamaño del audio: {len(audio_data)} bytes")

# Guardar en ubicación diferente
with open("backup/cancion.mp3", "wb") as f:
    f.write(audio_data)
```

---

## 🎤 Módulo: karaoke_generator.py

Generación profesional de videos de karaoke con sincronización de letras alimentada por IA.

### Funciones

#### `download_audio(youtube_url: str, output_path: str = "temp") -> Tuple[str, str]`

Descarga audio de video de YouTube con extracción de metadatos.

**Parámetros:**
- `youtube_url` (str): URL del video de YouTube
- `output_path` (str, opcional): Directorio de salida. Por defecto "temp"

**Retorna:**
- `Tuple[str, str]`: (nombre_archivo_audio, titulo_cancion)

**Lanza:**
- `subprocess.CalledProcessError`: Si el comando yt-dlp falla
- `FileNotFoundError`: Si no se puede crear el directorio de salida
- `ValueError`: Si la URL es inválida

**Ejemplo:**
```python
from karaoke_generator import download_audio

try:
    audio_file, title = download_audio(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        output_path="mi_audio"
    )
    print(f"Descargado: {title}")
    print(f"Archivo: {audio_file}")
except subprocess.CalledProcessError as e:
    print(f"Descarga falló: {e}")
```

**Detalles Técnicos:**
- **Formato**: MP3, 192kbps
- **Sanitización de Nombre**: Remueve caracteres especiales para compatibilidad del sistema de archivos
- **Preservación de Metadatos**: Extrae título, duración y otra información

#### `separate_vocals(audio_path: str, output_path: str = "temp") -> Tuple[str, str]`

Separación avanzada de voces usando el modelo IA Spleeter.

**Parámetros:**
- `audio_path` (str): Ruta al archivo de audio de entrada
- `output_path` (str, opcional): Directorio de salida. Por defecto "temp"

**Retorna:**
- `Tuple[str, str]`: (ruta_instrumental, ruta_voces)

**Lanza:**
- `FileNotFoundError`: Si no se encuentra el ejecutable de Spleeter
- `subprocess.CalledProcessError`: Si el proceso de separación falla

**Ejemplo:**
```python
from karaoke_generator import separate_vocals

try:
    instrumental, vocals = separate_vocals("temp/cancion.mp3")
    print(f"Instrumental: {instrumental}")
    print(f"Voces: {vocals}")
except FileNotFoundError:
    print("❌ Spleeter no instalado o no encontrado")
```

**Modelos de Spleeter:**
- **2stems**: voces/acompañamiento (por defecto)
- **4stems**: voces/batería/bajo/otros
- **5stems**: voces/batería/bajo/piano/otros

**Comparación de Calidad:**
```python
# Compromiso calidad vs velocidad del modelo
modelos = {
    '2stems': {'calidad': 'buena', 'velocidad': 'rápida', 'tamaño': '150MB'},
    '4stems': {'calidad': 'mejor', 'velocidad': 'media', 'tamaño': '300MB'},
    '5stems': {'calidad': 'mejor', 'velocidad': 'lenta', 'tamaño': '500MB'}
}
```

#### `generate_timed_lyrics(vocals_path: str) -> List[Dict[str, Union[str, float]]]`

Genera letras sincronizadas en tiempo usando Whisper AI.

**Parámetros:**
- `vocals_path` (str): Ruta al archivo de audio de voces

**Retorna:**
- `List[Dict]`: Lista de segmentos de letras con tiempo
  ```python
  [
      {
          'text': 'Never gonna give you up',
          'start': 15.2,  # segundos
          'end': 18.7     # segundos
      },
      # ... más segmentos
  ]
  ```

**Lanza:**
- `Exception`: Si la carga del modelo Whisper falla
- `RuntimeError`: Si el proceso de transcripción falla

**Ejemplo:**
```python
from karaoke_generator import generate_timed_lyrics

try:
    lyrics = generate_timed_lyrics("temp/vocals.wav")
    
    for segment in lyrics[:3]:  # Primeros 3 segmentos
        print(f"{segment['start']:.1f}s - {segment['end']:.1f}s: {segment['text']}")
        
    print(f"Segmentos totales: {len(lyrics)}")
except Exception as e:
    print(f"Transcripción falló: {e}")
```

**Modelos de Whisper:**
```python
modelos = {
    'tiny': {'tamaño': '39MB', 'velocidad': 'más rápida', 'precisión': 'más baja'},
    'base': {'tamaño': '74MB', 'velocidad': 'rápida', 'precisión': 'buena'},      # Por defecto
    'small': {'tamaño': '244MB', 'velocidad': 'media', 'precisión': 'mejor'},
    'medium': {'tamaño': '769MB', 'velocidad': 'lenta', 'precisión': 'alta'},
    'large': {'tamaño': '1550MB', 'velocidad': 'más lenta', 'precisión': 'más alta'}
}
```

#### `create_karaoke_video(instrumental_path: str, timed_lyrics: List[Dict], song_title: str, output_path: str = "output") -> None`

Crea video de karaoke profesional con superposición de letras sincronizadas.

**Parámetros:**
- `instrumental_path` (str): Ruta a la pista de audio instrumental
- `timed_lyrics` (List[Dict]): Letras sincronizadas de `generate_timed_lyrics()`
- `song_title` (str): Título para el nombre del archivo de salida
- `output_path` (str, opcional): Directorio de salida. Por defecto "output"

**Retorna:**
- `None`: El archivo de video se guarda en el directorio de salida

**Lanza:**
- `Exception`: Si el proceso de creación de video falla
- `MemoryError`: Si el sistema se queda sin memoria durante el procesamiento

**Ejemplo:**
```python
from karaoke_generator import create_karaoke_video

# Asumiendo que tienes las entradas requeridas
instrumental = "temp/cancion/accompaniment.wav"
lyrics = [
    {'text': 'Hola mundo', 'start': 0.0, 'end': 2.0},
    {'text': 'Esto es karaoke', 'start': 2.5, 'end': 5.0}
]
title = "Mi Canción de Karaoke"

try:
    create_karaoke_video(instrumental, lyrics, title)
    print("✅ ¡Video de karaoke creado exitosamente!")
except MemoryError:
    print("❌ No hay suficiente memoria - prueba video más corto o menor resolución")
```

**Especificaciones de Video:**
```python
# Configuraciones por defecto de video
VIDEO_CONFIG = {
    'resolution': (1280, 720),      # Resolución HD
    'framerate': 30,                # FPS
    'codec': 'libx264',            # Códec de video
    'audio_codec': 'aac',          # Códec de audio
    'bitrate': '5M',               # Bitrate de video
    'background_color': (25, 25, 112)  # Azul oscuro RGB
}

# Estilo de texto
TEXT_CONFIG = {
    'font': 'Arial',
    'fontsize': 60,
    'color': 'white',
    'highlight_color': 'yellow',
    'position': ('center', 0.65),  # Horizontal, Vertical (0.0-1.0)
    'outline': 2,                  # Ancho del contorno del texto
    'shadow': True                 # Sombra
}
```

---

## 📹 Módulo: movies.py

Descarga de videos de alta calidad desde múltiples plataformas.

### Funciones

#### `download_movie(url: str) -> str`

Descarga video en la mejor calidad disponible desde plataformas compatibles.

**Parámetros:**
- `url` (str): URL del video de plataforma compatible

**Retorna:**
- `str`: Ruta al archivo de video descargado

**Lanza:**
- `yt_dlp.DownloadError`: Si la descarga falla
- `OSError`: Si las operaciones del sistema de archivos fallan
- `ValueError`: Si la URL no es compatible

**Ejemplo:**
```python
from movies import download_movie

try:
    video_path = download_movie("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    print(f"Video descargado en: {video_path}")
    
    # Obtener información del archivo
    import os
    size_mb = os.path.getsize(video_path) / (1024 * 1024)
    print(f"Tamaño del archivo: {size_mb:.2f} MB")
    
except Exception as e:
    print(f"Descarga falló: {e}")
```

**Plataformas Compatibles:**
- YouTube
- Vimeo
- DailyMotion
- Twitch
- Facebook
- Instagram
- TikTok
- Twitter
- Reddit
- Y más de 100 más...

---

## ⚠️ Manejo de Errores

### Jerarquía de Excepciones

```python
# Excepciones base
class YouTubeDLError(Exception):
    """Excepción base para la suite de YouTube DL"""
    pass

class DownloadError(YouTubeDLError):
    """Se lanza cuando las operaciones de descarga fallan"""
    pass

class ProcessingError(YouTubeDLError):
    """Se lanza cuando el procesamiento de audio/video falla"""
    pass

class ConfigurationError(YouTubeDLError):
    """Se lanza cuando la configuración es inválida"""
    pass
```

### Patrones Comunes de Error

#### Errores Relacionados con la Red
```python
from yt_dlp import DownloadError
import requests.exceptions

def descarga_segura(url):
    try:
        return convert_to_audio(url)
    except DownloadError as e:
        if "HTTP Error 403" in str(e):
            print("❌ El video es privado o restringido")
        elif "Video unavailable" in str(e):
            print("❌ El video ha sido eliminado")
        elif "network" in str(e).lower():
            print("❌ Problema de conexión de red")
        else:
            print(f"❌ Descarga falló: {e}")
    except requests.exceptions.ConnectionError:
        print("❌ Sin conexión a internet")
```

---

## 🔧 Clases de Configuración

### AudioConfig

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class AudioConfig:
    """Configuración para operaciones de procesamiento de audio"""
    
    # Configuraciones de calidad
    format: str = 'mp3'              # mp3, wav, flac
    quality: str = '192'             # 96, 128, 192, 320 (kbps)
    sample_rate: int = 44100         # Hz
    channels: int = 2                # 1=mono, 2=estéreo
    
    # Configuraciones de procesamiento
    normalize_audio: bool = True      # Normalizar volumen
    noise_reduction: bool = False     # Aplicar reducción de ruido
    
    # Rutas
    output_dir: str = 'downloads'
    temp_dir: str = 'temp'
    
    def __post_init__(self):
        """Validar configuración"""
        valid_formats = ['mp3', 'wav', 'flac', 'ogg']
        if self.format not in valid_formats:
            raise ValueError(f"Formato inválido: {self.format}")
            
        if not (96 <= int(self.quality) <= 320):
            raise ValueError(f"Calidad inválida: {self.quality}")

# Ejemplo de uso
config = AudioConfig(format='wav', quality='320')
```

---

## 💡 Ejemplos

### Pipeline Completo de Karaoke

```python
from karaoke_generator import (
    download_audio, 
    separate_vocals, 
    generate_timed_lyrics, 
    create_karaoke_video
)
from pathlib import Path
import os

def crear_karaoke_desde_url(youtube_url: str, output_dir: str = "output") -> str:
    """
    Pipeline completo de creación de karaoke.
    
    Args:
        youtube_url: URL del video de YouTube
        output_dir: Directorio para el video final
        
    Returns:
        Ruta al video de karaoke creado
    """
    
    # Asegurar que los directorios existen
    Path("temp").mkdir(exist_ok=True)
    Path(output_dir).mkdir(exist_ok=True)
    
    try:
        # Paso 1: Descargar audio
        print("📥 Descargando audio...")
        audio_path, song_title = download_audio(youtube_url)
        
        # Paso 2: Separar voces
        print("🎵 Separando voces...")
        instrumental_path, vocals_path = separate_vocals(audio_path)
        
        # Paso 3: Generar letras
        print("📝 Generando letras...")
        timed_lyrics = generate_timed_lyrics(vocals_path)
        
        if not timed_lyrics:
            raise Exception("No se pudieron generar letras")
        
        # Paso 4: Crear video
        print("🎬 Creando video de karaoke...")
        create_karaoke_video(instrumental_path, timed_lyrics, song_title, output_dir)
        
        # Retornar ruta del video final
        safe_title = "".join(c for c in song_title if c.isalnum() or c in ' -_').strip()
        video_path = os.path.join(output_dir, f"{safe_title}_karaoke.mp4")
        
        print(f"✅ Video de karaoke creado: {video_path}")
        return video_path
        
    except Exception as e:
        print(f"❌ Pipeline falló: {e}")
        raise

# Uso
video_path = crear_karaoke_desde_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
```

Esta referencia completa de API proporciona toda la información necesaria para integrar y extender la suite de YouTube DL. Cada función incluye parámetros detallados, valores de retorno, condiciones de error y ejemplos prácticos para uso inmediato.