# Suite de Procesamiento de Audio y Video de YouTube DL

Un completo conjunto de herramientas de Python para descargar, procesar y crear contenido de karaoke desde YouTube y otras plataformas de video. Esta suite incluye tres aplicaciones principales para diferentes necesidades de procesamiento multimedia.

![Versión de Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)
![Licencia](https://img.shields.io/badge/license-MIT-green.svg)
![Mantenimiento](https://img.shields.io/badge/Maintained%3F-yes-green.svg)

## 📋 Tabla de Contenidos

- [Visión General](#visión-general)
- [Características](#características)
- [Instalación](#instalación)
- [Inicio Rápido](#inicio-rápido)
- [Aplicaciones](#aplicaciones)
  - [Procesador de Audio (app.py)](#procesador-de-audio-apppy)
  - [Generador de Karaoke](#generador-de-karaoke-karaoke_generatorpy)
  - [Descargador de Películas](#descargador-de-películas-moviespy)
- [Ejemplos de Uso](#ejemplos-de-uso)
- [Configuración](#configuración)
- [Solución de Problemas](#solución-de-problemas)
- [Contribuir](#contribuir)
- [Licencia](#licencia)

## 🎯 Visión General

Este proyecto proporciona una solución completa para:
- **Extracción de Audio**: Convierte videos de YouTube a archivos de audio de alta calidad
- **Separación de Voz**: Separa las voces de las pistas instrumentales
- **Creación de Karaoke**: Genera videos de karaoke sincronizados con letras
- **Descarga de Videos**: Descarga videos de varias plataformas

## ✨ Características

### 🎵 Procesamiento de Audio
- Extracción de audio de alta calidad (MP3 192kbps)
- Separación avanzada de voz/música usando Librosa
- Soporte para múltiples formatos de audio
- Capacidades de procesamiento por lotes

### 🎤 Generación de Karaoke
- Transcripción automática de letras usando Whisper AI
- Generación de subtítulos sincronizados
- Estilos de video personalizables
- Múltiples formatos de exportación

### 📹 Descarga de Videos
- Soporte para más de 100 plataformas de video
- Selección automática de la mejor calidad
- Capacidades de descarga masiva
- Seguimiento de progreso

### 🔧 Características Técnicas
- Compatibilidad multiplataforma (Windows, macOS, Linux)
- Manejo robusto de errores
- Arquitectura modular
- Registro extensivo
- Procesamiento eficiente en memoria

## 🚀 Instalación

### Prerrequisitos

- Python 3.7 o superior
- FFmpeg (requerido para procesamiento de audio/video)
- Al menos 2GB de espacio libre en disco

### Dependencias del Sistema

#### macOS
```bash
# Instalar Homebrew si no está instalado
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar FFmpeg
brew install ffmpeg
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg python3-pip python3-venv
```

#### Windows
```bash
# Instalar FFmpeg usando Chocolatey
choco install ffmpeg

# O descargar desde: https://ffmpeg.org/download.html
```

### Configuración del Entorno Python

1. **Clonar o descargar el proyecto**
```bash
git clone <repository-url>
cd "Youtube DL"
```

2. **Crear entorno virtual**
```bash
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

3. **Instalar dependencias de Python**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Instalar Spleeter (para generación de karaoke)**
```bash
# Crear entorno de Spleeter
python3 -m venv spleeter_env
source spleeter_env/bin/activate  # En Windows: spleeter_env\Scripts\activate
pip install spleeter[tensorflow]
deactivate
```

### Verificación
```bash
# Probar instalaciones
python3 -c "import yt_dlp, librosa, moviepy; print('¡Todas las dependencias instaladas correctamente!')"
```

## 🏃‍♂️ Inicio Rápido

### Extracción Básica de Audio
```bash
python3 app.py
# Ingresa la URL de YouTube cuando se te solicite
```

### Generar Video de Karaoke
```bash
python3 karaoke_generator.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Descargar Video
```bash
python3 movies.py
# Ingresa la URL del video cuando se te solicite
```

## 📱 Aplicaciones

### Procesador de Audio (app.py)

**Propósito**: Convertir videos de YouTube a audio y separar voces de instrumentales.

#### Características:
- **Extracción de Audio de Alta Calidad**: Convierte videos a MP3 de 192kbps
- **Separación de Voz**: Usa separación harmónico-percusiva
- **Procesamiento Automático**: Maneja todo el proceso automáticamente

#### Uso:
```bash
python3 app.py
```

#### Flujo del Proceso:
1. Solicita URL de YouTube
2. Descarga audio en la mejor calidad disponible
3. Convierte a formato MP3
4. Separa voces y música de fondo
5. Guarda archivos en el directorio `downloads/`

#### Archivos de Salida:
- `downloads/{titulo_video}.mp3` - Audio original
- `downloads/voice.wav` - Voces extraídas
- `downloads/background.wav` - Música de fondo

#### Ejemplo de Código:
```python
from app import convert_to_audio, separate_voice

# Convertir video a audio
audio_file = convert_to_audio("https://youtube.com/watch?v=...")

# Separar voces del fondo
separate_voice(audio_file)
```

### Generador de Karaoke (karaoke_generator.py)

**Propósito**: Crear videos de karaoke profesionales con letras sincronizadas.

#### Características:
- **Transcripción Alimentada por IA**: Usa Whisper para letras precisas
- **Separación de Fuentes**: Crea pistas instrumentales limpias
- **Generación de Video**: Produce videos de karaoke MP4
- **Estilos Personalizables**: Fuentes, colores y diseños ajustables

#### Uso:
```bash
python3 karaoke_generator.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### Pipeline del Proceso:

1. **Descarga de Audio**
   - Extrae audio de YouTube
   - Guarda como MP3 en directorio `temp/`

2. **Separación Vocal**
   - Usa Spleeter AI para separación limpia
   - Genera `vocals.wav` y `accompaniment.wav`

3. **Generación de Letras**
   - Transcribe voces usando Whisper AI
   - Crea letras sincronizadas en tiempo
   - Agrupa palabras en líneas legibles

4. **Creación de Video**
   - Crea video HD de 1280x720
   - Añade superposición de subtítulos sincronizados
   - Exporta como MP4 con audio instrumental

#### Salida:
- `output/{titulo_cancion}_karaoke.mp4` - Video de karaoke final
- `temp/{titulo_cancion}/` - Archivos intermedios

### Descargador de Películas (movies.py)

**Propósito**: Descargar videos de varias plataformas en la mejor calidad disponible.

#### Características:
- **Soporte Multi-Plataforma**: YouTube, Vimeo, DailyMotion y más de 100 sitios
- **Selección de Calidad**: Selecciona automáticamente la mejor calidad disponible
- **Nomenclatura Inteligente**: Maneja caracteres especiales en nombres de archivo
- **Detección de Formato**: Preserva el formato de video original

#### Uso:
```bash
python3 movies.py
```

#### Plataformas Compatibles:
- YouTube
- Vimeo  
- DailyMotion
- Twitch
- Facebook
- Instagram
- TikTok
- Y muchas más...

## 💡 Ejemplos de Uso

### Ejemplo 1: Crear Karaoke de Canción Popular
```bash
# Descargar y crear karaoke de una canción popular
python3 karaoke_generator.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Salida: Rick_Astley_Never_Gonna_Give_You_Up_karaoke.mp4
```

### Ejemplo 2: Extraer Audio para Remix
```bash
# Ejecutar el procesador de audio
python3 app.py
# Ingresa: https://www.youtube.com/watch?v=dQw4w9WgXcQ

# Archivos creados:
# - downloads/Never_Gonna_Give_You_Up.mp3 (original)
# - downloads/voice.wav (solo voces)  
# - downloads/background.wav (instrumental)
```

### Ejemplo 3: Procesamiento por Lotes
```python
# Crear un script de procesamiento por lotes
import os
from karaoke_generator import main as generate_karaoke

urls = [
    "https://www.youtube.com/watch?v=VIDEO1",
    "https://www.youtube.com/watch?v=VIDEO2",
    "https://www.youtube.com/watch?v=VIDEO3"
]

for url in urls:
    try:
        os.system(f'python3 karaoke_generator.py "{url}"')
        print(f"✅ Procesado: {url}")
    except Exception as e:
        print(f"❌ Falló: {url} - {e}")
```

## ⚙️ Configuración

### Variables de Entorno
Crea un archivo `.env` para configuraciones personalizadas:

```bash
# archivo .env
DOWNLOAD_PATH=/ruta/personalizada/downloads
TEMP_PATH=/ruta/personalizada/temp
OUTPUT_PATH=/ruta/personalizada/output
MAX_DOWNLOAD_SIZE=1000000000  # Límite de 1GB
WHISPER_MODEL=base  # tiny, base, small, medium, large
```

### Configuraciones de Aplicación

#### Configuración de app.py
```python
# Configuraciones de calidad de audio
AUDIO_QUALITY = '192'  # 96, 128, 192, 320
AUDIO_FORMAT = 'mp3'   # mp3, wav, flac

# Configuraciones de procesamiento
USE_GPU = False  # Establecer en True si CUDA está disponible
NOISE_REDUCTION = True
```

#### Configuración de karaoke_generator.py
```python
# Configuraciones de salida de video
VIDEO_RESOLUTION = (1920, 1080)  # 4K: (3840, 2160)
VIDEO_FRAMERATE = 30
VIDEO_BITRATE = '5M'

# Selección de modelo Whisper
WHISPER_MODEL = 'base'  # Opciones: tiny, base, small, medium, large
# tiny: más rápido, menos preciso
# large: más lento, más preciso

# Estilos de subtítulos
SUBTITLE_FONT = 'Arial'
SUBTITLE_SIZE = 60
SUBTITLE_COLOR = 'white'
SUBTITLE_OUTLINE = 2
```

## 🐛 Solución de Problemas

### Problemas Comunes y Soluciones

#### 1. FFmpeg No Encontrado
```bash
# Error: ffmpeg no encontrado
# Solución:
sudo apt install ffmpeg  # Ubuntu
brew install ffmpeg      # macOS
choco install ffmpeg     # Windows
```

#### 2. Problemas de Instalación de Spleeter
```bash
# Error: Compatibilidad de TensorFlow
# Solución: Usar versiones específicas
pip install tensorflow==2.8.0
pip install spleeter==2.3.0
```

#### 3. Fallos de Descarga de YouTube
```bash
# Error: No se puede descargar
# Solución: Actualizar yt-dlp
pip install --upgrade yt-dlp

# O usar formato alternativo
python3 -c "
import yt_dlp
ydl_opts = {'format': 'worst'}  # Probar calidad más baja
"
```

#### 4. Problemas de Memoria
```bash
# Error: Sin memoria
# Solución: Reducir tamaño del modelo Whisper
# Editar karaoke_generator.py:
model = stable_whisper.load_model('tiny')  # En lugar de 'base'
```

## 📊 Métricas de Rendimiento

### Tiempos de Procesamiento Típicos

| Tarea | Tamaño de Archivo | Tiempo de Procesamiento | Hardware |
|-------|-------------------|------------------------|----------|
| Descarga de Audio | 4MB (canción de 3 min) | 10-30 segundos | Internet Estándar |
| Separación Vocal | Audio de 4MB | 30-60 segundos | CPU i5 |
| Generación de Letras | Canción de 3 min | 1-3 minutos | CPU + Whisper base |
| Creación de Video | 1080p 3 min | 2-5 minutos | CPU i5 |
| **Pipeline Total** | **Canción de 3 min** | **4-9 minutos** | **PC Estándar** |

### Requisitos de Hardware

| Componente | Mínimo | Recomendado | Óptimo |
|------------|---------|-------------|---------|
| CPU | 2 núcleos, 2GHz | 4 núcleos, 3GHz | 8+ núcleos, 3.5GHz |
| RAM | 4GB | 8GB | 16GB+ |
| Almacenamiento | 5GB libres | 20GB libres | SSD 50GB+ |
| GPU | Ninguna | GTX 1060 | RTX 3070+ |

## 🤝 Contribuir

¡Damos la bienvenida a las contribuciones! Así es como empezar:

### Configuración de Desarrollo
```bash
# Hacer fork del repositorio
git clone https://github.com/tuusuario/youtube-dl-suite.git
cd youtube-dl-suite

# Crear entorno de desarrollo
python3 -m venv dev_env
source dev_env/bin/activate

# Instalar dependencias de desarrollo
pip install -r requirements.txt
pip install pytest black flake8 mypy
```

### Estilo de Código
- Seguir las guías PEP 8
- Usar type hints donde sea posible
- Añadir docstrings a todas las funciones
- Longitud máxima de línea: 88 caracteres

### Pruebas
```bash
# Ejecutar pruebas
pytest tests/

# Ejecutar con cobertura
pytest --cov=. tests/

# Verificación de tipos
mypy *.py

# Formateo de código
black *.py
```

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.

### Licencias de Terceros
- **yt-dlp**: Dominio Público (Unlicense)
- **FFmpeg**: LGPL v2.1+
- **Spleeter**: Licencia MIT
- **Whisper**: Licencia MIT
- **MoviePy**: Licencia MIT
- **Librosa**: Licencia ISC

## 🙏 Reconocimientos

- **Equipo de yt-dlp** por la excelente biblioteca de descarga de videos
- **Deezer Research** por Spleeter de separación de fuentes de audio
- **OpenAI** por el reconocimiento de voz Whisper
- **Desarrolladores de Librosa** por las herramientas de procesamiento de audio
- **Equipo de MoviePy** por las capacidades de edición de video

## 📞 Soporte

### Obtener Ayuda
- 📖 Revisa esta documentación primero
- 🐛 [Reportar errores](https://github.com/username/repo/issues)
- 💡 [Solicitar características](https://github.com/username/repo/issues)
- 💬 [Unirse a discusiones](https://github.com/username/repo/discussions)

### Comunidad
- Discord: [Únete a nuestro servidor](https://discord.gg/invite)
- Reddit: [r/YouTubeDL](https://reddit.com/r/youtubedl)
- Stack Overflow: Etiqueta con `youtube-dl-suite`

---

**Hecho con ❤️ por el Equipo de YouTube DL Suite**

*Última actualización: 2024*