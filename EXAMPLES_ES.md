# 💡 Ejemplos y Casos de Uso

Este documento proporciona ejemplos prácticos y casos de uso del mundo real para la Suite de Procesamiento de Audio y Video de YouTube DL.

## 📋 Tabla de Contenidos

- [Ejemplos de Inicio Rápido](#ejemplos-de-inicio-rápido)
- [Ejemplos de Procesamiento de Audio](#ejemplos-de-procesamiento-de-audio)
- [Ejemplos de Generación de Karaoke](#ejemplos-de-generación-de-karaoke)
- [Ejemplos de Descarga de Video](#ejemplos-de-descarga-de-video)
- [Casos de Uso Avanzados](#casos-de-uso-avanzados)
- [Ejemplos de Integración](#ejemplos-de-integración)
- [Scripts de Automatización](#scripts-de-automatización)

## 🚀 Ejemplos de Inicio Rápido

### Ejemplo 1: Extraer Audio de Video de YouTube
```bash
# Extracción simple de audio
python3 app.py
# Cuando se solicite, ingresa: https://www.youtube.com/watch?v=dQw4w9WgXcQ

# Resultado: 
# - downloads/Never_Gonna_Give_You_Up.mp3 (audio original)
# - downloads/voice.wav (solo voces)
# - downloads/background.wav (instrumental)
```

### Ejemplo 2: Crear Tu Primer Video de Karaoke
```bash
# Generar video de karaoke con letras
python3 karaoke_generator.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Resultado:
# - output/Never_Gonna_Give_You_Up_karaoke.mp4 (video de karaoke)
# - temp/ carpeta con archivos intermedios
```

### Ejemplo 3: Descargar Video en Mejor Calidad
```bash
# Descargar archivo de video
python3 movies.py
# Cuando se solicite, ingresa: https://www.youtube.com/watch?v=dQw4w9WgXcQ

# Resultado:
# - downloads/Never_Gonna_Give_You_Up.mp4 (archivo de video)
```

## 🎵 Ejemplos de Procesamiento de Audio

### Extracción Básica de Audio

```python
from app import convert_to_audio, separate_voice
import os

# Ejemplo 1: Extraer audio de múltiples fuentes
urls = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # YouTube
    "https://vimeo.com/123456789",                   # Vimeo
    "https://dailymotion.com/video/x123456"          # DailyMotion
]

for i, url in enumerate(urls, 1):
    print(f"\n=== Procesando Video {i} ===")
    try:
        # Convertir a audio
        audio_path = convert_to_audio(url)
        print(f"✅ Audio extraído: {audio_path}")
        
        # Obtener tamaño del archivo
        size_mb = os.path.getsize(audio_path) / (1024 * 1024)
        print(f"📁 Tamaño del archivo: {size_mb:.2f} MB")
        
        # Separar voces
        separate_voice(audio_path)
        print("✅ Separación de voz completada")
        
    except Exception as e:
        print(f"❌ Error procesando {url}: {e}")
```

## 🎤 Ejemplos de Generación de Karaoke

### Creación Básica de Karaoke

```python
from karaoke_generator import (
    download_audio, 
    separate_vocals, 
    generate_timed_lyrics, 
    create_karaoke_video
)

def crear_karaoke_con_configuraciones(youtube_url: str, configuraciones_personalizadas: dict = None):
    """Crear video de karaoke con configuraciones personalizadas."""
    
    # Configuraciones por defecto
    configuraciones = {
        'modelo_whisper': 'base',
        'resolucion_video': (1280, 720),
        'tamano_fuente': 60,
        'color_fondo': (25, 25, 112),
        'color_texto': 'white',
        'color_resaltado': 'yellow'
    }
    
    # Actualizar con configuraciones personalizadas
    if configuraciones_personalizadas:
        configuraciones.update(configuraciones_personalizadas)
    
    print(f"🎬 Creando karaoke para: {youtube_url}")
    
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
        
        if timed_lyrics:
            # Paso 4: Crear video
            print("🎬 Creando video de karaoke...")
            create_karaoke_video(instrumental_path, timed_lyrics, song_title)
            print("✅ ¡Creación de karaoke completada!")
        else:
            print("❌ No se pudieron generar letras.")
            
    except Exception as e:
        print(f"❌ Error: {e}")

# Ejemplo de uso
crear_karaoke_con_configuraciones("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
```

## 📹 Ejemplos de Descarga de Video

### Descarga Multi-Plataforma

```python
from movies import download_movie
import os
from urllib.parse import urlparse

def descargador_inteligente_video(urls: list, directorio_destino: str = "downloads") -> dict:
    """Descargar videos de múltiples plataformas."""
    
    os.makedirs(directorio_destino, exist_ok=True)
    
    resultados = {
        'descargas_exitosas': [],
        'descargas_fallidas': [],
        'tamano_total_mb': 0,
        'plataformas_usadas': set()
    }
    
    for url in urls:
        print(f"\n📥 Procesando: {url}")
        
        try:
            # Identificar plataforma
            domain = urlparse(url).netloc.lower()
            plataforma = 'YouTube' if 'youtube.com' in domain else 'Otra'
            
            resultados['plataformas_usadas'].add(plataforma)
            
            # Descargar video
            video_path = download_movie(url)
            
            # Obtener información del archivo
            file_size = os.path.getsize(video_path)
            size_mb = file_size / (1024 * 1024)
            
            resultados['descargas_exitosas'].append({
                'url': url,
                'plataforma': plataforma,
                'ruta_archivo': video_path,
                'tamano_mb': round(size_mb, 2)
            })
            
            resultados['tamano_total_mb'] += size_mb
            print(f"✅ Descargado: {os.path.basename(video_path)} ({size_mb:.2f} MB)")
            
        except Exception as e:
            resultados['descargas_fallidas'].append({
                'url': url,
                'plataforma': plataforma,
                'error': str(e)
            })
            print(f"❌ Falló: {e}")
    
    return resultados

# Ejemplo de uso
urls_mixtas = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://vimeo.com/148751763"
]

resultados_descarga = descargador_inteligente_video(urls_mixtas)
print(f"\n📊 Resumen: {len(resultados_descarga['descargas_exitosas'])} exitosas, {len(resultados_descarga['descargas_fallidas'])} fallidas")
```

## 🔧 Casos de Uso Avanzados

### Flujo de Trabajo de Producción Musical

```python
import librosa
import soundfile as sf
import numpy as np
from app import convert_to_audio, separate_voice

def pipeline_produccion_musical(youtube_url: str) -> dict:
    """Pipeline completo de producción musical desde video de YouTube."""
    
    print("🎵 Iniciando pipeline de producción musical...")
    
    # Paso 1: Extraer audio
    audio_path = convert_to_audio(youtube_url)
    
    # Paso 2: Separar stems
    separate_voice(audio_path)
    
    # Paso 3: Cargar pistas separadas
    vocals, sr = librosa.load('downloads/voice.wav')
    instruments, _ = librosa.load('downloads/background.wav')
    
    # Paso 4: Análisis de audio
    tempo, beats = librosa.beat.beat_track(y=vocals + instruments, sr=sr)
    
    # Paso 5: Crear stems de producción
    vocals_normalized = librosa.util.normalize(vocals)
    instruments_normalized = librosa.util.normalize(instruments)
    
    # Exportar stems
    stems = {
        'vocals_dry': vocals_normalized,
        'instruments_full': instruments_normalized,
        'full_mix': vocals_normalized * 0.7 + instruments_normalized * 0.8
    }
    
    rutas_stems = {}
    for nombre_stem, audio_data in stems.items():
        ruta_archivo = f'downloads/production_{nombre_stem}.wav'
        sf.write(ruta_archivo, audio_data, sr)
        rutas_stems[nombre_stem] = ruta_archivo
    
    return {
        'tempo_bpm': float(tempo),
        'duracion_segundos': len(vocals) / sr,
        'stems_produccion': rutas_stems
    }

# Ejemplo de uso
reporte = pipeline_produccion_musical("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
print(f"🎵 Tempo: {reporte['tempo_bpm']:.1f} BPM")
print(f"⏱️ Duración: {reporte['duracion_segundos']:.1f} segundos")
```

## 🤖 Ejemplos de Integración

### Aplicación Web Flask Simple

```python
from flask import Flask, request, jsonify, send_file
import os
import threading
from datetime import datetime
import uuid

app = Flask(__name__)
trabajos_procesamiento = {}

@app.route('/api/procesar_video', methods=['POST'])
def procesar_video():
    """Endpoint API para iniciar procesamiento de video."""
    
    data = request.json
    youtube_url = data.get('url')
    
    if not youtube_url:
        return jsonify({'error': 'URL es requerida'}), 400
    
    job_id = str(uuid.uuid4())
    
    trabajos_procesamiento[job_id] = {
        'status': 'iniciado',
        'url': youtube_url,
        'creado_en': datetime.now().isoformat()
    }
    
    # Iniciar procesamiento en segundo plano
    def procesar_en_segundo_plano():
        try:
            from karaoke_generator import main as generate_karaoke
            import sys
            
            original_argv = sys.argv
            sys.argv = ['karaoke_generator.py', youtube_url]
            generate_karaoke()
            sys.argv = original_argv
            
            trabajos_procesamiento[job_id]['status'] = 'completado'
        except Exception as e:
            trabajos_procesamiento[job_id]['status'] = 'error'
            trabajos_procesamiento[job_id]['error'] = str(e)
    
    thread = threading.Thread(target=procesar_en_segundo_plano)
    thread.daemon = True
    thread.start()
    
    return jsonify({'job_id': job_id, 'status': 'iniciado'}), 202

@app.route('/api/estado/<job_id>')
def obtener_estado(job_id):
    """Obtener estado del trabajo."""
    if job_id not in trabajos_procesamiento:
        return jsonify({'error': 'Trabajo no encontrado'}), 404
    
    return jsonify(trabajos_procesamiento[job_id])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## 🔧 Scripts de Automatización

### Procesamiento por Lotes

```bash
#!/bin/bash
# Procesador de playlist automatizado

PLAYLIST_URL="$1"
TIPO_SALIDA="$2"

if [ -z "$PLAYLIST_URL" ]; then
    echo "Uso: $0 <playlist_url> <tipo_salida>"
    echo "Tipos de salida: karaoke, audio, video"
    exit 1
fi

echo "📥 Extrayendo URLs de playlist..."
yt-dlp --flat-playlist --get-id "$PLAYLIST_URL" > playlist_ids.txt

# Convertir IDs a URLs
sed 's/^/https:\/\/www.youtube.com\/watch?v=/' playlist_ids.txt > playlist_urls.txt

echo "📊 Se encontraron $(wc -l < playlist_urls.txt) videos"

# Procesar cada video
while read url; do
    echo "🎬 Procesando: $url"
    
    case "$TIPO_SALIDA" in
        "karaoke")
            python3 karaoke_generator.py "$url"
            ;;
        "audio")
            echo "$url" | python3 app.py
            ;;
        "video")
            echo "$url" | python3 movies.py
            ;;
    esac
    
    if [ $? -eq 0 ]; then
        echo "✅ Completado: $url"
    else
        echo "❌ Error: $url"
    fi
    
done < playlist_urls.txt

echo "📊 Procesamiento de playlist completado"
rm playlist_ids.txt playlist_urls.txt
```

### Script de Monitoreo

```python
#!/usr/bin/env python3
import psutil
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def monitorear_procesamiento():
    """Monitorear uso de recursos durante procesamiento."""
    
    while True:
        # Verificar uso de CPU y memoria
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        # Buscar procesos de nuestra aplicación
        procesos_activos = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] == 'python3':
                    cmdline = ' '.join(proc.info['cmdline'])
                    if any(script in cmdline for script in ['app.py', 'karaoke_generator.py', 'movies.py']):
                        procesos_activos.append(proc.info['pid'])
            except:
                continue
        
        # Registrar estado
        logger.info(f"CPU: {cpu_percent}%, Memoria: {memory.percent}%, Procesos activos: {len(procesos_activos)}")
        
        # Alertas
        if cpu_percent > 90:
            logger.warning("⚠️ Alto uso de CPU detectado")
        if memory.percent > 85:
            logger.warning("⚠️ Alto uso de memoria detectado")
        
        time.sleep(30)

if __name__ == "__main__":
    monitorear_procesamiento()
```

Esta documentación en español proporciona ejemplos prácticos y completos para todos los aspectos de la Suite de YouTube DL, desde uso básico hasta automatización avanzada e integración en aplicaciones web.