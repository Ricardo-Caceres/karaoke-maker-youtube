import os
import sys
import subprocess
import torch

# Force venv site-packages
venv_site_packages = os.path.join(os.getcwd(), "spleeter_env", "lib", "python3.9", "site-packages")
if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)

import stable_whisper
from audio_separator.separator import Separator

# --- CONFIGURATION ---
WHISPER_MODEL = "large-v3"  
VOCAL_MODEL = "UVR-MDX-NET-Voc_FT.onnx" 
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
# ---------------------

def find_yt_dlp():
    """Find the best yt-dlp executable available."""
    # Check if 'yt-dlp' in current PATH is working (not giving 403 on a test)
    # But for simplicity, we'll look for common locations and check versions
    try:
        # Check system yt-dlp first if it's likely to be newer
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
        return "".join([c for c in raw_title if c.isalnum() or c in (" ", "-", "_")]).strip()
    except:
        return "karaoke_song"

def download_media(url, audio_path, video_path):
    if os.path.exists(audio_path) and os.path.exists(video_path):
        print(">> Media present.")
        return
    print(f"Downloading HQ media...")
    
    yt_dlp_cmd = find_yt_dlp()
    # Common arguments to help with 403 Forbidden errors
    retry_args = ["--no-cache-dir", "--extractor-args", "youtube:player_client=android_web,web"]
    
    try:
        # First attempt: standard download
        subprocess.run([yt_dlp_cmd, "--no-playlist", "-x", "--audio-format", "wav", "-o", audio_path, url], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n[!] yt-dlp first attempt failed. Retrying with alternative arguments...")
        try:
            # Second attempt: with retry arguments
            subprocess.run([yt_dlp_cmd, "--no-playlist", "-x", "--audio-format", "wav", *retry_args, "-o", audio_path, url], check=True)
        except subprocess.CalledProcessError:
            print(f"\n[!] CRITICAL ERROR: yt-dlp failed completely with 403 Forbidden or other error.")
            print(f"    Current yt-dlp: {yt_dlp_cmd}")
            print(f"    Please update yt-dlp: 'pip install --upgrade yt-dlp'")
            print(f"    Note: If you are using Python 3.9, you may need to update to Python 3.10+ to get the latest fixes.")
            raise e

    try:
        # Video download
        subprocess.run([yt_dlp_cmd, "--no-playlist", "-f", "bestvideo[height>=720][ext=mp4]/bestvideo[ext=mp4]/best[ext=mp4]", "-o", video_path, url], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n[!] yt-dlp video download failed. Retrying with alternative arguments...")
        try:
            subprocess.run([yt_dlp_cmd, "--no-playlist", "-f", "bestvideo[height>=720][ext=mp4]/bestvideo[ext=mp4]/best[ext=mp4]", *retry_args, "-o", video_path, url], check=True)
        except subprocess.CalledProcessError:
            print(f"    Error: Failed to download video format.")
            raise e

def separate_lead_vocals(audio_path, inst_path, voc_path, output_dir):
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

def generate_ultra_precise_karaoke(audio_path, vocals_path, output_ass, safe_title):
    """Generates lyrics with two-pass refinement for maximum accuracy."""
    print(f"Transcribing LEAD VOCALS on {DEVICE.upper()} (Two-Pass Mode)...")
    model = stable_whisper.load_model(WHISPER_MODEL, device=DEVICE)
    
    # Pass 1: High-beam transcription
    # We use vocals_path (isolated voice) for better word recognition
    prompt = f"Canción: {safe_title} de Nacho Vegas y Christina Rosenvinge. Transcripción poética y literal en español."
    
    print("  [Pass 1] Initial Transcription...")
    result = model.transcribe(
        vocals_path, 
        fp16=False, 
        language='es', 
        initial_prompt=prompt,
        beam_size=5, # Higher beam size for better word choice
        best_of=5,
        condition_on_previous_text=False,
        regroup=True
    )
    
    # Pass 2: Alignment Refinement
    # This re-checks every word against the audio to fix timestamps and missed phonemes
    print("  [Pass 2] Refining and Aligning phonemes...")
    result = model.align(vocals_path, result, language='es')
    model.refine(vocals_path, result)
    
    segments = result.segments
    if not segments: return False

    print(f"SUCCESS: Captured {len(segments)} lines with high precision.")
    
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Active,Arial,52,&H00FFFFFF,&H0000FFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,3,0,5,10,10,10,1
Style: Inactive,Arial,38,&H70FFFFFF,&H70FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,5,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    with open(output_ass, 'w', encoding='utf-8') as f:
        f.write(header)
        Y_B, Y_C, Y_T, Y_O = 460, 360, 260, 160
        for i, seg in enumerate(segments):
            t_s, t_e = seg.start, seg.end
            t_n = segments[i+1].start if i < len(segments) - 1 else t_e + 2
            t_an = segments[i+2].start if i < len(segments) - 2 else t_n + 2
            t_a = segments[i-1].start if i > 0 else 0
            
            k_text = "".join([f"{{\\k{int((w.end - w.start) * 100)}}}{w.word}" for w in seg.words])
            
            if t_s > t_a:
                f.write(f"Dialogue: 0,{format_timestamp(t_a)},{format_timestamp(t_s)},Inactive,,0,0,0,,{{\\pos(640,{Y_B})}}{{\\fad(400,0)}}{seg.text.strip()}\n")
            f.write(f"Dialogue: 1,{format_timestamp(t_s)},{format_timestamp(t_n)},Active,,0,0,0,,{{\\move(640,{Y_B},640,{Y_C},0,400)}}{k_text}\n")
            f.write(f"Dialogue: 0,{format_timestamp(t_n)},{format_timestamp(t_an)},Inactive,,0,0,0,,{{\\move(640,{Y_C},640,{Y_T},0,400)}}{seg.text.strip()}\n")
            f.write(f"Dialogue: 0,{format_timestamp(t_an)},{format_timestamp(t_an+1)},Inactive,,0,0,0,,{{\\move(640,{Y_T},640,{Y_O},0,400)}}{{\\fad(0,400)}}{seg.text.strip()}\n")
        f.flush()
        os.fsync(f.fileno())
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 karaoke_generator.py <url> [vol] [mode]")
        sys.exit(1)
        
    url = sys.argv[1]
    vocal_volume = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
    mode = sys.argv[3].lower() if len(sys.argv) > 3 else "full"
    
    os.makedirs("temp", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    try:
        safe_title = get_safe_title(url)
        audio_wav = os.path.join("temp", f"{safe_title}.wav")
        video_mp4 = os.path.join("temp", f"{safe_title}_video.mp4")
        inst_wav = os.path.join("temp", f"{safe_title}_inst.wav")
        voc_wav = os.path.join("temp", f"{safe_title}_voc.wav")
        ass_path = os.path.join("temp", f"{safe_title}.ass")

        if mode in ("full", "lyrics"):
            download_media(url, audio_wav, video_mp4)
            separate_lead_vocals(audio_wav, inst_wav, voc_wav, "temp")
            # We now pass both original and isolated vocals for maximum precision
            generate_ultra_precise_karaoke(audio_wav, voc_wav, ass_path, safe_title)
        
        if not os.path.exists(ass_path):
            print(f"Error: Missing {ass_path}")
            return

        print("--- FINAL RENDER ---")
        mixed_audio = os.path.join("temp", f"{safe_title}_final.wav")
        subprocess.run(["ffmpeg", "-y", "-i", inst_wav, "-i", voc_wav, "-filter_complex", f"[1:a]volume={vocal_volume}[v];[0:a][v]amix=inputs=2:duration=first", "-ac", "2", mixed_audio], check=True, capture_output=True)
        
        output_video = os.path.join("output", f"{safe_title}_PRECISION_KARAOKE.mp4")
        abs_ass = os.path.abspath(ass_path).replace(":", "\\:").replace("'", "\\'")
        subprocess.run(["ffmpeg", "-y", "-i", video_mp4, "-i", mixed_audio, "-vf", f"ass='{abs_ass}'", "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", "-b:a", "320k", "-map", "0:v:0", "-map", "1:a:0", "-shortest", output_video], check=True)
        
        print(f"\n¡ULTRA-PRECISION COMPLETADA! Video en: {output_video}")

    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()