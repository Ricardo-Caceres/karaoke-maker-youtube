import os
import sys
import subprocess
import torch
import argparse

# Evitar error de duplicado de libiomp5
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Force venv site-packages
venv_site_packages = os.path.join(os.getcwd(), "spleeter_env", "lib", "python3.9", "site-packages")
if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)

import stable_whisper
import lyricsgenius
from audio_separator.separator import Separator
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# --- CONFIGURATION ---
WHISPER_MODEL = "large-v3"
VOCAL_MODEL = "UVR-MDX-NET-Voc_FT.onnx" 
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
GENIUS_TOKEN = os.getenv("GENIUS_TOKEN")
# ---------------------

def find_yt_dlp():
    """Find the best yt-dlp executable available."""
    try:
        system_yt_dlp = "/usr/local/bin/yt-dlp"
        if os.path.exists(system_yt_dlp):
            return system_yt_dlp
    except:
        pass
    return "yt-dlp"

def get_safe_title(youtube_url):
    try:
        yt_dlp_cmd = find_yt_dlp()
        command = [yt_dlp_cmd, "--get-title", "--no-playlist", youtube_url]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        raw_title = result.stdout.strip()
        # Limpieza básica para nombres de archivo
        return "".join([c for c in raw_title if c.isalnum() or c in (" ", "-", "_")]).strip(), raw_title
    except:
        return "karaoke_song", "karaoke_song"

def fetch_lyrics_from_genius(song_title_raw):
    """Intenta descargar la letra de Genius para Alineación Forzada (100% Precisión)."""
    if not GENIUS_TOKEN:
        print("  [Genius] No Token found. Skipping Auto-Lyrics.")
        return None
    
    try:
        print(f"  [Genius] Searching for: {song_title_raw}...")
        genius = lyricsgenius.Genius(GENIUS_TOKEN, verbose=False, remove_section_headers=True)
        # Limpiamos el título quitando cosas como "(Official Video)", "HD", etc.
        clean_title = song_title_raw.split("(")[0].split("[")[0].strip()
        song = genius.search_song(clean_title)
        
        if song:
            print(f"  [Genius] Match found: {song.title} by {song.artist}")
            # Limpieza profunda de la letra
            lyrics = song.lyrics
            # Genius a veces añade cosas raras al inicio o final de la letra, quitamos el header de "Lyrics"
            if "Lyrics" in lyrics:
                lyrics = lyrics.split("Lyrics", 1)[1]
            # Quitar números al final de la letra (indicadores de contribución de Genius)
            import re
            lyrics = re.sub(r"\d+Embed$", "", lyrics).strip()
            return lyrics
        else:
            print("  [Genius] No matches found.")
            return None
    except Exception as e:
        print(f"  [Genius] Error: {e}")
        return None

def download_media(url, audio_path, video_path, quality_height=720):
    if os.path.exists(audio_path) and os.path.exists(video_path):
        print(">> Media present.")
        return
    print(f"Downloading HQ media (Target Quality: {quality_height}p)...")
    
    yt_dlp_cmd = find_yt_dlp()
    retry_args = ["--no-cache-dir", "--extractor-args", "youtube:player_client=android_web,web"]
    
    try:
        subprocess.run([yt_dlp_cmd, "--no-playlist", "-x", "--audio-format", "wav", "-o", audio_path, url], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n[!] yt-dlp first attempt failed. Retrying with alternative arguments...")
        try:
            subprocess.run([yt_dlp_cmd, "--no-playlist", "-x", "--audio-format", "wav", *retry_args, "-o", audio_path, url], check=True)
        except subprocess.CalledProcessError:
            print(f"\n[!] CRITICAL ERROR: yt-dlp failed completely.")
            raise e

    v_format = f"bestvideo[height>={quality_height}][ext=mp4]/bestvideo[ext=mp4]/best[ext=mp4]"
    try:
        subprocess.run([yt_dlp_cmd, "--no-playlist", "-f", v_format, "-o", video_path, url], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n[!] yt-dlp video download failed. Retrying...")
        try:
            subprocess.run([yt_dlp_cmd, "--no-playlist", "-f", v_format, *retry_args, "-o", video_path, url], check=True)
        except subprocess.CalledProcessError:
            print(f"    Error: Failed to download video format.")
            raise e

def separate_lead_vocals(audio_path, inst_path, voc_path, output_dir):
    """Mantenemos esta lógica intacta ya que la separación es perfecta."""
    if os.path.exists(inst_path) and os.path.exists(voc_path):
        print(">> Audio already separated.")
        return
    print(f"Separating Lead Vocals with MDX-Net (Ultra-Quality)...")
    separator = Separator(output_dir=output_dir, output_format="wav")
    separator.load_model(VOCAL_MODEL)
    output_files = separator.separate(audio_path)
    os.rename(os.path.join(output_dir, output_files[0]), inst_path)
    os.rename(os.path.join(output_dir, output_files[1]), voc_path)

def format_timestamp(seconds):
    if seconds < 0: seconds = 0
    h, m = int(seconds // 3600), int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def generate_ultra_precise_karaoke(audio_path, vocals_path, output_ass, safe_title, lyrics_content=None):
    """Generates lyrics with cinematic scroll effect and high sensitivity."""
    print(f"Transcribing LEAD VOCALS on {DEVICE.upper()} (STABLE-MODE)...")
    
    # Volvemos al motor original para evitar crashes en este entorno
    model = stable_whisper.load_model(WHISPER_MODEL, device=DEVICE)
    
    # Prompt Maestro: Instrucciones precisas para evitar omisiones
    master_prompt = (
        f"Transcripción literal para karaoke de la canción: {safe_title}. "
        "No omitas ninguna palabra, incluso si son susurros, gritos o repeticiones. "
        "Escribe cada sílaba que escuches. El idioma es español. "
        "Formato poético, sin etiquetas de tiempo en el texto."
    )
    
    if lyrics_content:
        print("  [Option 3] Forced Alignment mode ACTIVE (Using Genius/Text Lyrics).")
        # Alineación Forzada: Tenemos la letra, solo buscamos los tiempos
        result = model.align(vocals_path, lyrics_content, language='es')
    else:
        print("  [Option 1] High-Sensitivity Transcription with Stable-Whisper...")
        result = model.transcribe(
            vocals_path, 
            fp16=False,
            language='es', 
            initial_prompt=master_prompt,
            beam_size=5,
            best_of=5,
            suppress_silence=False,
            vad=True,
            regroup=True
        )
    
    print("  [Refining] Phoneme-level synchronization...")
    model.refine(vocals_path, result)
    
    print("  Regrouping for cinematic flow...")
    result.regroup('sl')
    # Separar si hay un silencio de más de 0.4s
    result.split_by_gap(0.4)
    # Separar por puntuación fuerte
    result.split_by_punctuation([",", ".", "?", "!", ";", ":", "..."])
    
    # NUEVO: Forzamos el corte si la línea es muy larga (máximo 6 palabras)
    # Esto evita el amontonamiento que viste en el screenshot
    try:
        result.split_by_length(max_words=6)
    except:
        pass
        
    result.remove_no_word_segments()
    result.segments = [s for s in result.segments if (s.end - s.start) > 0.1]
    
    segments = result.segments
    if not segments: 
        print("  [!] Error: No se detectaron segmentos de voz.")
        return False

    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,42,&H00FF0000,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,1,5,30,30,60,1
Style: Active,Arial,48,&H00FF0000,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,4,1,5,30,30,60,1
"""
    with open(output_ass, 'w', encoding='utf-8') as f:
        f.write(header + "\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
        
        # Reagrupamiento ultra-agresivo para evitar amontonamiento
        result.regroup('sl')
        result.split_by_gap(0.3) # Casi cualquier pausa crea nueva línea
        result.split_by_punctuation([",", ".", "?", "!", ";", ":", "..."])
        
        try:
            result.split_by_length(max_words=5) # Máximo 5 palabras por línea para claridad total
        except:
            pass
            
        result.remove_no_word_segments()
        result.segments = [s for s in result.segments if (s.end - s.start) > 0.1]
        
        segments = result.segments
        if not segments: 
            print("  [!] Error: No se detectaron segmentos de voz.")
            return False

        for i, seg in enumerate(segments):
            s_start, s_end = seg.start, seg.end
            
            # Anticipación de 4 segundos
            v_start = max(0, s_start - 4.0)
            v_end = s_end + 1.2
            
            # Sincronización del resaltado
            wait_offset = int((s_start - v_start) * 100)
            k_text = f"{{\\k{wait_offset}}}"
            
            for word in seg.words:
                chars = list(word.word)
                if not chars: continue
                total_word_dur = int((word.end - word.start) * 100)
                char_dur = total_word_dur // len(chars)
                remainder = total_word_dur % len(chars)
                for idx, char in enumerate(chars):
                    dur = char_dur + (1 if idx < remainder else 0)
                    k_text += f"{{\\k{dur}}}{char}"
                k_text += " "

            # Coordenadas: Zona Central Compacta (Smooth Action Zone)
            y_in, y_out = 580, 120
            scroll_move = f"\\move(640,{y_in},640,{y_out})"
            
            fade = "\\fad(800,500)"
            
            t_sing_start = int((s_start - v_start) * 1000)
            t_sing_end = int((s_end - v_start) * 1000)
            zoom = f"\\t({t_sing_start},{t_sing_end},\\fscx115\\fscy115)"
            
            effect_tags = f"{{{scroll_move}{fade}{zoom}}}"
            f.write(f"Dialogue: 0,{format_timestamp(v_start)},{format_timestamp(v_end)},Active,,0,0,0,,{effect_tags}{k_text.strip()}\n")
            
        f.flush()
        os.fsync(f.fileno())
    return True

def main():
    parser = argparse.ArgumentParser(description="Ultra-Precision Karaoke Generator with Faster-Whisper & Genius")
    parser.add_argument("url", help="YouTube URL to process")
    parser.add_argument("-v", "--volume", type=float, default=0.0, help="Vocal volume adjustment (default: 0.0)")
    parser.add_argument("-m", "--mode", choices=["full", "lyrics", "render"], default="full", help="Processing mode (default: full)")
    parser.add_argument("-q", "--quality", type=int, default=720, help="Target video quality/height (default: 720)")
    parser.add_argument("-l", "--lyrics", help="Path to a text file with lyrics for Forced Alignment")
    
    args = parser.parse_args()
    
    os.makedirs("temp", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    try:
        safe_title, raw_title = get_safe_title(args.url)
        audio_wav = os.path.join("temp", f"{safe_title}.wav")
        video_mp4 = os.path.join("temp", f"{safe_title}_video.mp4")
        inst_wav = os.path.join("temp", f"{safe_title}_inst.wav")
        voc_wav = os.path.join("temp", f"{safe_title}_voc.wav")
        ass_path = os.path.join("temp", f"{safe_title}.ass")

        lyrics_content = None

        if args.mode in ("full", "lyrics"):
            download_media(args.url, audio_wav, video_mp4, quality_height=args.quality)
            separate_lead_vocals(audio_wav, inst_wav, voc_wav, "temp")
            
            # Buscar letra en Genius si no se provee por argumento
            if args.lyrics and os.path.exists(args.lyrics):
                with open(args.lyrics, 'r', encoding='utf-8') as f:
                    lyrics_content = f.read().strip()
            else:
                lyrics_content = fetch_lyrics_from_genius(raw_title)

            generate_ultra_precise_karaoke(audio_wav, voc_wav, ass_path, safe_title, lyrics_content=lyrics_content)
        
        if not os.path.exists(ass_path):
            print(f"Error: No se pudo generar el archivo de subtítulos {ass_path}")
            return

        print("--- FINAL RENDER ---")
        mixed_audio = os.path.join("temp", f"{safe_title}_final.wav")
        subprocess.run(["ffmpeg", "-y", "-i", inst_wav, "-i", voc_wav, "-filter_complex", f"[1:a]volume={args.volume}[v];[0:a][v]amix=inputs=2:duration=first", "-ac", "2", mixed_audio], check=True, capture_output=True)
        
        output_video = os.path.join("output", f"{safe_title}_PRECISION_KARAOKE.mp4")
        abs_ass = os.path.abspath(ass_path).replace(":", "\\:").replace("'", "\\'")
        subprocess.run(["ffmpeg", "-y", "-i", video_mp4, "-i", mixed_audio, "-vf", f"ass='{abs_ass}'", "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", "-b:a", "320k", "-map", "0:v:0", "-map", "1:a:0", "-shortest", output_video], check=True)
        
        print(f"\n¡ULTRA-PRECISION COMPLETADA! Video en: {output_video}")

    except Exception as e:
        print(f"\nError Crítico: {e}")

if __name__ == "__main__":
    main()
