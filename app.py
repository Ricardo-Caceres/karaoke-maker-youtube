import subprocess
import librosa
import soundfile as sf
import os

def find_yt_dlp():
    """Find the best yt-dlp executable available."""
    try:
        system_yt_dlp = "/usr/local/bin/yt-dlp"
        if os.path.exists(system_yt_dlp):
            return system_yt_dlp
    except:
        pass
    return "yt-dlp"

def convert_to_audio(url):
    os.makedirs('downloads', exist_ok=True)
    yt_dlp_cmd = find_yt_dlp()
    
    # Get title first
    try:
        title_cmd = [yt_dlp_cmd, "--get-title", "--no-playlist", url]
        title = subprocess.check_output(title_cmd, text=True).strip()
    except:
        title = "audio_file"

    audio_file = os.path.join('downloads', f"{title}.mp3")
    
    if os.path.exists(audio_file):
        print(f">> Audio present: {audio_file}")
        return audio_file

    print(f"Downloading audio from {url}...")
    # Common arguments to help with 403 Forbidden errors
    retry_args = ["--no-cache-dir", "--extractor-args", "youtube:player_client=android_web,web"]
    
    try:
        subprocess.run([yt_dlp_cmd, "--no-playlist", "-x", "--audio-format", "mp3", "-o", audio_file, url], check=True)
    except subprocess.CalledProcessError:
        print(f"\n[!] yt-dlp first attempt failed. Retrying with alternative arguments...")
        try:
            subprocess.run([yt_dlp_cmd, "--no-playlist", "-x", "--audio-format", "mp3", *retry_args, "-o", audio_file, url], check=True)
        except subprocess.CalledProcessError as e:
            print(f"    Error: Failed to download audio. Please update yt-dlp (pip install --upgrade yt-dlp).")
            raise e
            
    return audio_file

# convert a video to audio
youtubeVideo = input("Enter the youtube video link: ")
audio_file = convert_to_audio(youtubeVideo)

# create a function to separate the voice from the background music:
def separate_voice(audio_file):
    y, sr = librosa.load(audio_file)
    y_harmonic, y_percussive = librosa.effects.hpss(y)
    sf.write('downloads/voice.wav', y_harmonic, sr)
    sf.write('downloads/background.wav', y_percussive, sr)

# separate the voice from the background music
separate_voice(audio_file)

# create a function to download the audio:
def download_audio(audio_file):
    with open(audio_file, 'rb') as f:
        return f.read()

# download the audio
audio = download_audio(audio_file)
print(audio)

# https://www.youtube.com/watch?v=vbZ-VLuDTIw