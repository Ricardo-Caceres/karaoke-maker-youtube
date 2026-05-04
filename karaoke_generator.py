import os
import sys
import subprocess
import re
import torch
import argparse
import stable_whisper
import lyricsgenius
from audio_separator.separator import Separator
from dotenv import load_dotenv
from PIL import ImageFont

# Evitar error de duplicado de libiomp5
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Force venv site-packages
venv_site_packages = os.path.join(os.getcwd(), "spleeter_env", "lib", "python3.9", "site-packages")
if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)

# Cargar variables de entorno desde .env
load_dotenv()

# --- CONFIGURATION ---
WHISPER_MODEL = "large-v3"
VOCAL_MODEL = "UVR-MDX-NET-Voc_FT.onnx" 
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
GENIUS_TOKEN = os.getenv("GENIUS_TOKEN")
# ---------------------

def get_text_width(text, size=48):
    if not text: return 0
    # Intentar rutas comunes de Arial en macOS
    paths = [
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Microsoft/Arial.ttf",
        "Arial.ttf"
    ]
    font = None
    for p in paths:
        try:
            font = ImageFont.truetype(p, size)
            break
        except:
            continue
    
    try:
        if font:
            if hasattr(font, 'getlength'):
                return font.getlength(text)
            else:
                return font.getbbox(text)[2]
        else:
            # Fallback proporcional si no hay fuente: ~0.5 del tamaño por carácter
            return len(text) * (size * 0.52)
    except:
        return len(text) * (size * 0.5)

LETTER_PATTERN = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]")
STRONG_VOWELS = set("aáeéoó")
ALLOWED_CONSONANT_ONSETS = {
    "bl", "br", "cl", "cr", "dr", "fl", "fr",
    "gl", "gr", "pl", "pr", "tr", "tl", "ch", "ll", "rr"
}

def _is_vowel(char):
    return char.lower() in "aeiouáéíóúü"

def _split_vowel_group(vowel_group):
    if not vowel_group:
        return []
    pieces = [vowel_group[0]]
    for char in vowel_group[1:]:
        prev = pieces[-1][-1]
        prev_l = prev.lower()
        char_l = char.lower()
        is_hiatus = (
            prev_l in ("í", "ú") or
            char_l in ("í", "ú") or
            (prev_l in STRONG_VOWELS and char_l in STRONG_VOWELS)
        )
        if is_hiatus:
            pieces.append(char)
        else:
            pieces[-1] += char
    return pieces

def _consonant_split_index(cluster):
    n = len(cluster)
    if n <= 1:
        return 0
    cluster_l = cluster.lower()
    if n == 2:
        return 0 if cluster_l in ALLOWED_CONSONANT_ONSETS else 1
    if n == 3:
        return 1 if cluster_l[1:] in ALLOWED_CONSONANT_ONSETS else 2
    return (n - 2) if cluster_l[-2:] in ALLOWED_CONSONANT_ONSETS else (n - 1)

def split_spanish_syllables(word):
    if not word:
        return []
    if not any(_is_vowel(c) for c in word):
        return [word]

    syllables = []
    i = 0
    while i < len(word):
        onset_start = i
        while i < len(word) and not _is_vowel(word[i]):
            i += 1

        if i >= len(word):
            if syllables:
                syllables[-1] += word[onset_start:]
            else:
                syllables.append(word[onset_start:])
            break

        vowel_start = i
        while i < len(word) and _is_vowel(word[i]):
            i += 1
        vowel_group = word[vowel_start:i]
        nuclei = _split_vowel_group(vowel_group)

        current = word[onset_start:vowel_start] + nuclei[0]
        for nucleus in nuclei[1:]:
            syllables.append(current)
            current = nucleus

        cons_start = i
        while i < len(word) and not _is_vowel(word[i]):
            i += 1
        consonants = word[cons_start:i]

        if i >= len(word):
            current += consonants
            syllables.append(current)
            break

        split_idx = _consonant_split_index(consonants)
        current += consonants[:split_idx]
        syllables.append(current)
        i = cons_start + split_idx

    return [s for s in syllables if s]

def split_token_into_syllables(token):
    if not token:
        return []

    spans = list(re.finditer(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+", token))
    if not spans:
        return [token]

    chunks = []
    cursor = 0
    for match in spans:
        prefix = token[cursor:match.start()]
        core_word = match.group(0)
        syllables = split_spanish_syllables(core_word) or [core_word]
        if prefix:
            syllables[0] = prefix + syllables[0]
        chunks.extend(syllables)
        cursor = match.end()

    if cursor < len(token):
        suffix = token[cursor:]
        if chunks:
            chunks[-1] += suffix
        else:
            chunks.append(suffix)

    return [chunk for chunk in chunks if chunk]

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
        return "".join([c for c in raw_title if c.isalnum() or c in (" ", "-", "_")]).strip(), raw_title
    except:
        return "karaoke_song", "karaoke_song"

def fetch_lyrics_from_genius(song_title_raw):
    if not GENIUS_TOKEN:
        print("  [Genius] No Token found. Skipping Auto-Lyrics.")
        return None
    
    try:
        print(f"  [Genius] Searching for: {song_title_raw}...")
        genius = lyricsgenius.Genius(GENIUS_TOKEN, verbose=False, remove_section_headers=True)
        clean_title = song_title_raw.split("(")[0].split("[")[0].strip()
        song = genius.search_song(clean_title)
        
        if song:
            print(f"  [Genius] Match found: {song.title} by {song.artist}")
            lyrics = song.lyrics
            if "Lyrics" in lyrics:
                lyrics = lyrics.split("Lyrics", 1)[1]
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
    
    v_format = f"bestvideo[height<={quality_height}][ext=mp4]+bestaudio[ext=m4a]/best[height<={quality_height}][ext=mp4]"
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
    if os.path.exists(inst_path) and os.path.exists(voc_path):
        print(">> Audio already separated.")
        return
    
    print(f"Separating VOCALS with High-Fidelity Model ({VOCAL_MODEL})...")
    separator = Separator(
        output_dir=output_dir,
        model_file_dir=os.path.join(os.getcwd(), "pretrained_models"),
        output_format="WAV"
    )
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
    """Generates lyrics with fixed lines at the bottom and a bouncing ball."""
    print(f"Transcribing LEAD VOCALS on {DEVICE.upper()} (BOUNCING BALL PRO MODE)...")
    model = stable_whisper.load_model(WHISPER_MODEL, device=DEVICE)
    
    if lyrics_content:
        print("  [Option 3] Forced Alignment mode ACTIVE (Using Genius/Text Lyrics).")
        result = model.align(vocals_path, lyrics_content, language='es')
    else:
        print("  [Option 1] High-Sensitivity Transcription with Stable-Whisper...")
        result = model.transcribe(vocals_path, language='es', regroup=True)

    print("  [Refining] Phoneme-level synchronization...")
    model.refine(vocals_path, result)
    
    result.regroup('sl')
    result.split_by_gap(0.4)
    result.split_by_punctuation([",", ".", "?", "!", ";", ":", "..."])
    
    try:
        result.split_by_length(max_words=5) 
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
Style: Default,Arial,42,&H00FF0000,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,1,2,30,30,60,1
Style: Active,Arial,48,&H00FF0000,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,4,1,2,30,30,60,1
Style: Ball,Arial,40,&H0000FFFF,&H0000FFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,1,2,0,0,0,1
"""
    with open(output_ass, 'w', encoding='utf-8') as f:
        f.write(header + "\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
        
        for i, seg in enumerate(segments):
            s_start, s_end = seg.start, seg.end
            y_pos = 660 if (i % 2 == 0) else 600
            
            v_start = max(0, s_start - 1.5)
            if i > 0:
                v_start = max(v_start, segments[i-1].end)
            v_end = s_end + 1.0
            
            wait_offset = int((s_start - v_start) * 100)
            k_text = f"{{\\k{wait_offset}}}"
            
            cumulative_text = ""
            syllable_data = []
            
            for word in seg.words:
                raw_word = word.word or ""
                if not raw_word:
                    continue

                w_start = word.start if word.start is not None else s_start
                w_end = word.end if word.end is not None else w_start
                if w_end <= w_start:
                    continue

                total_word_cs = max(1, int(round((w_end - w_start) * 100)))
                syllable_chunks = split_token_into_syllables(raw_word)
                if total_word_cs < len(syllable_chunks):
                    syllable_chunks = [raw_word]
                if not syllable_chunks:
                    syllable_chunks = [raw_word]

                weights = [max(1, len(LETTER_PATTERN.findall(chunk))) for chunk in syllable_chunks]
                weight_sum = sum(weights) if weights else 1
                syllable_cs = [(total_word_cs * w) // weight_sum for w in weights]
                remainder_cs = total_word_cs - sum(syllable_cs)
                for r in range(remainder_cs):
                    syllable_cs[r % len(syllable_cs)] += 1

                chunk_start = w_start
                for s_idx, (chunk, chunk_cs) in enumerate(zip(syllable_chunks, syllable_cs)):
                    chunk_cs = max(1, chunk_cs)
                    chunk_end = w_end if s_idx == len(syllable_chunks) - 1 else min(w_end, chunk_start + (chunk_cs / 100.0))

                    chunk_width = get_text_width(chunk, size=48)
                    width_before = get_text_width(cumulative_text, size=48)
                    center_x_offset = width_before + (chunk_width / 2)

                    syllable_data.append({
                        'start': chunk_start,
                        'end': chunk_end,
                        'x': center_x_offset,
                        'dur': max(0.01, chunk_end - chunk_start)
                    })
                    k_text += f"{{\\k{chunk_cs}}}{chunk}"
                    cumulative_text += chunk
                    chunk_start = chunk_end

            # Escribir línea de texto
            f.write(f"Dialogue: 1,{format_timestamp(v_start)},{format_timestamp(v_end)},Active,,0,0,0,,{{\\pos(640,{y_pos})}}{k_text.strip()}\n")
            
            # --- PELOTA: REBOTE VERTICAL TIPO PING-PONG POR SÍLABA ---
            total_seg_width = get_text_width(cumulative_text, size=48)
            start_x = 640 - (total_seg_width / 2)
            bottom_y = y_pos - 45
            top_y = y_pos - 105
            current_y = bottom_y
            
            for idx, s in enumerate(syllable_data):
                abs_x = start_x + s['x']
                s_start = s['start']
                s_end = s['end']
                if s_end <= s_start:
                    continue

                target_y = top_y if (idx % 2 == 0) else bottom_y

                if idx == 0:
                    prep_start = max(v_start, s_start - 0.25)
                    f.write(f"Dialogue: 2,{format_timestamp(prep_start)},{format_timestamp(s_start)},Ball,,0,0,0,,{{\\an5\\pos({abs_x},{current_y})\\fscx0\\fscy0\\t(\\fscx100\\fscy100)}}●\\n")

                # Rebote vertical por sílaba (la duración real define la velocidad)
                f.write(f"Dialogue: 2,{format_timestamp(s_start)},{format_timestamp(s_end)},Ball,,0,0,0,,{{\\an5\\move({abs_x},{current_y},{abs_x},{target_y})\\fscx120\\fscy120}}●\\n")
                current_y = target_y

                # Desplazamiento horizontal entre sílabas sin cambiar altura
                if idx < len(syllable_data) - 1:
                    next_s = syllable_data[idx + 1]
                    next_x = start_x + next_s['x']
                    if next_s['start'] > s_end:
                        f.write(f"Dialogue: 2,{format_timestamp(s_end)},{format_timestamp(next_s['start'])},Ball,,0,0,0,,{{\\an5\\move({abs_x},{current_y},{next_x},{current_y})}}●\\n")
                else:
                    fade_end = min(v_end, s_end + 0.25)
                    f.write(f"Dialogue: 2,{format_timestamp(s_end)},{format_timestamp(fade_end)},Ball,,0,0,0,,{{\\an5\\pos({abs_x},{current_y})\\t(\\fscx0\\fscy0)}}●\\n")

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
