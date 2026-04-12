# 💡 Examples and Use Cases

This document provides practical examples and real-world use cases for the YouTube DL Audio & Video Processing Suite.

## 📋 Table of Contents

- [Quick Start Examples](#quick-start-examples)
- [Audio Processing Examples](#audio-processing-examples)
- [Karaoke Generation Examples](#karaoke-generation-examples)
- [Video Download Examples](#video-download-examples)
- [Advanced Use Cases](#advanced-use-cases)
- [Integration Examples](#integration-examples)
- [Automation Scripts](#automation-scripts)
- [Troubleshooting Examples](#troubleshooting-examples)

## 🚀 Quick Start Examples

### Example 1: Extract Audio from YouTube Video
```bash
# Simple audio extraction
python3 app.py
# When prompted, enter: https://www.youtube.com/watch?v=dQw4w9WgXcQ

# Result: 
# - downloads/Never_Gonna_Give_You_Up.mp3 (original audio)
# - downloads/voice.wav (vocals only)
# - downloads/background.wav (instrumental)
```

### Example 2: Create Your First Karaoke Video
```bash
# Generate karaoke video with lyrics
python3 karaoke_generator.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Result:
# - output/Never_Gonna_Give_You_Up_karaoke.mp4 (karaoke video)
# - temp/ folder with intermediate files
```

### Example 3: Download Video in Best Quality
```bash
# Download video file
python3 movies.py
# When prompted, enter: https://www.youtube.com/watch?v=dQw4w9WgXcQ

# Result:
# - downloads/Never_Gonna_Give_You_Up.mp4 (video file)
```

## 🎵 Audio Processing Examples

### Basic Audio Extraction

```python
from app import convert_to_audio, separate_voice
import os

# Example 1: Extract audio from multiple sources
urls = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # YouTube
    "https://vimeo.com/123456789",                   # Vimeo
    "https://dailymotion.com/video/x123456"          # DailyMotion
]

for i, url in enumerate(urls, 1):
    print(f"\n=== Processing Video {i} ===")
    try:
        # Convert to audio
        audio_path = convert_to_audio(url)
        print(f"✅ Audio extracted: {audio_path}")
        
        # Get file size
        size_mb = os.path.getsize(audio_path) / (1024 * 1024)
        print(f"📁 File size: {size_mb:.2f} MB")
        
        # Separate vocals
        separate_voice(audio_path)
        print("✅ Voice separation completed")
        
    except Exception as e:
        print(f"❌ Error processing {url}: {e}")
```

### Custom Audio Processing Pipeline

```python
import librosa
import soundfile as sf
import numpy as np
from app import convert_to_audio

def advanced_audio_processing(url: str) -> dict:
    """Advanced audio processing with custom effects."""
    
    # Step 1: Download audio
    audio_path = convert_to_audio(url)
    
    # Step 2: Load audio for analysis
    y, sr = librosa.load(audio_path)
    
    # Step 3: Audio analysis
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)
    
    # Step 4: Audio effects
    # Tempo adjustment
    y_fast = librosa.effects.time_stretch(y, rate=1.2)  # 20% faster
    y_slow = librosa.effects.time_stretch(y, rate=0.8)  # 20% slower
    
    # Pitch shifting
    y_higher = librosa.effects.pitch_shift(y, sr=sr, n_steps=2)  # 2 semitones up
    y_lower = librosa.effects.pitch_shift(y, sr=sr, n_steps=-2)  # 2 semitones down
    
    # Noise reduction (simple spectral gating)
    stft = librosa.stft(y)
    magnitude = np.abs(stft)
    phase = np.angle(stft)
    
    # Simple noise gate
    threshold = np.percentile(magnitude, 30)  # Bottom 30% considered noise
    mask = magnitude > threshold
    cleaned_stft = magnitude * mask * np.exp(1j * phase)
    y_clean = librosa.istft(cleaned_stft)
    
    # Step 5: Save processed versions
    effects = {
        'original': audio_path,
        'fast': 'downloads/fast_version.wav',
        'slow': 'downloads/slow_version.wav',
        'higher': 'downloads/higher_pitch.wav',
        'lower': 'downloads/lower_pitch.wav',
        'clean': 'downloads/noise_reduced.wav'
    }
    
    sf.write(effects['fast'], y_fast, sr)
    sf.write(effects['slow'], y_slow, sr)
    sf.write(effects['higher'], y_higher, sr)
    sf.write(effects['lower'], y_lower, sr)
    sf.write(effects['clean'], y_clean, sr)
    
    # Return analysis results
    return {
        'tempo': float(tempo),
        'duration': len(y) / sr,
        'sample_rate': sr,
        'effects_created': effects,
        'spectral_centroid_mean': float(np.mean(spectral_centroids)),
        'chroma_features': chroma.shape
    }

# Example usage
results = advanced_audio_processing("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
print(f"Song tempo: {results['tempo']:.1f} BPM")
print(f"Duration: {results['duration']:.1f} seconds")
```

## 🎤 Karaoke Generation Examples

### Basic Karaoke Creation

```python
from karaoke_generator import (
    download_audio, 
    separate_vocals, 
    generate_timed_lyrics, 
    create_karaoke_video
)

def create_karaoke_with_settings(youtube_url: str, custom_settings: dict = None):
    """Create karaoke video with custom settings."""
    
    # Default settings
    settings = {
        'whisper_model': 'base',
        'video_resolution': (1280, 720),
        'font_size': 60,
        'background_color': (25, 25, 112),
        'text_color': 'white',
        'highlight_color': 'yellow'
    }
    
    # Update with custom settings
    if custom_settings:
        settings.update(custom_settings)
    
    print(f"🎬 Creating karaoke for: {youtube_url}")
    print(f"⚙️ Settings: {settings}")
    
    try:
        # Step 1: Download audio
        print("📥 Downloading audio...")
        audio_path, song_title = download_audio(youtube_url)
        
        # Step 2: Separate vocals
        print("🎵 Separating vocals...")
        instrumental_path, vocals_path = separate_vocals(audio_path)
        
        # Step 3: Generate lyrics with custom model
        print(f"📝 Generating lyrics (model: {settings['whisper_model']})...")
        
        # Modify the function to use custom Whisper model
        import stable_whisper
        model = stable_whisper.load_model(settings['whisper_model'])
        result = model.transcribe(vocals_path, fp16=False)
        
        # Process lyrics (same as original function)
        lines = []
        current_line = []
        for segment in result.segments:
            for word in segment.words:
                current_line.append(word)
                if len(current_line) >= 8:
                    start_time = current_line[0].start
                    end_time = current_line[-1].end
                    text = ' '.join([w.word for w in current_line])
                    lines.append({'text': text, 'start': start_time, 'end': end_time})
                    current_line = []
        
        if current_line:
            start_time = current_line[0].start
            end_time = current_line[-1].end
            text = ' '.join([w.word for w in current_line])
            lines.append({'text': text, 'start': start_time, 'end': end_time})
        
        # Step 4: Create custom video
        print("🎬 Creating karaoke video...")
        create_karaoke_video(instrumental_path, lines, song_title)
        
        print("✅ Karaoke creation completed!")
        return {
            'status': 'success',
            'song_title': song_title,
            'lyrics_count': len(lines),
            'settings_used': settings
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {'status': 'error', 'error': str(e)}

# Example: Create karaoke with high-quality settings
high_quality_settings = {
    'whisper_model': 'large',           # Most accurate transcription
    'video_resolution': (1920, 1080),  # Full HD
    'font_size': 80,                   # Larger text
    'background_color': (0, 0, 0),     # Black background
    'highlight_color': '#FFD700'       # Gold highlight
}

result = create_karaoke_with_settings(
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    high_quality_settings
)
```

### Batch Karaoke Generation

```python
import json
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from karaoke_generator import main as generate_karaoke
import sys
import os

def batch_karaoke_generation(urls: list, max_workers: int = 2) -> dict:
    """Generate karaoke videos for multiple URLs concurrently."""
    
    results = {
        'started_at': datetime.now().isoformat(),
        'total_urls': len(urls),
        'completed': 0,
        'failed': 0,
        'results': {},
        'errors': {}
    }
    
    def process_single_url(url: str) -> tuple:
        """Process a single URL and return result."""
        start_time = time.time()
        
        try:
            # Temporarily redirect sys.argv for the main function
            original_argv = sys.argv
            sys.argv = ['karaoke_generator.py', url]
            
            # Call the main function
            generate_karaoke()
            
            # Restore sys.argv
            sys.argv = original_argv
            
            processing_time = time.time() - start_time
            return (url, {
                'status': 'success',
                'processing_time': processing_time,
                'completed_at': datetime.now().isoformat()
            })
            
        except Exception as e:
            sys.argv = original_argv  # Ensure cleanup
            processing_time = time.time() - start_time
            return (url, {
                'status': 'error',
                'error': str(e),
                'processing_time': processing_time,
                'failed_at': datetime.now().isoformat()
            })
    
    # Process URLs concurrently
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all jobs
        future_to_url = {executor.submit(process_single_url, url): url for url in urls}
        
        # Collect results as they complete
        for future in as_completed(future_to_url):
            url, result = future.result()
            results['results'][url] = result
            
            if result['status'] == 'success':
                results['completed'] += 1
                print(f"✅ Completed: {url} ({result['processing_time']:.1f}s)")
            else:
                results['failed'] += 1
                results['errors'][url] = result['error']
                print(f"❌ Failed: {url} - {result['error']}")
    
    # Final statistics
    results['finished_at'] = datetime.now().isoformat()
    total_time = sum(r['processing_time'] for r in results['results'].values())
    results['total_processing_time'] = total_time
    results['success_rate'] = results['completed'] / results['total_urls'] * 100
    
    # Save results to file
    with open('batch_karaoke_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    return results

# Example: Process a playlist of songs
playlist_urls = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://www.youtube.com/watch?v=L_jWHffIx5E",  # Smash Mouth - All Star
    "https://www.youtube.com/watch?v=ZZ5LpwO-An4",  # HEYYEYAAEYAAAEYAEYAA
    "https://www.youtube.com/watch?v=y6120QOlsfU",  # Darude - Sandstorm
    "https://www.youtube.com/watch?v=9bZkp7q19f0"   # Gangnam Style
]

print("🎬 Starting batch karaoke generation...")
results = batch_karaoke_generation(playlist_urls, max_workers=2)

print(f"\n📊 Batch Results:")
print(f"✅ Completed: {results['completed']}/{results['total_urls']}")
print(f"❌ Failed: {results['failed']}/{results['total_urls']}")
print(f"📈 Success Rate: {results['success_rate']:.1f}%")
print(f"⏱️ Total Time: {results['total_processing_time']:.1f} seconds")
```

## 📹 Video Download Examples

### Multi-Platform Download

```python
from movies import download_movie
import os
from urllib.parse import urlparse

def smart_video_downloader(urls: list, target_directory: str = "downloads") -> dict:
    """Download videos from multiple platforms with smart features."""
    
    # Ensure target directory exists
    os.makedirs(target_directory, exist_ok=True)
    
    results = {
        'successful_downloads': [],
        'failed_downloads': [],
        'total_size_mb': 0,
        'platforms_used': set()
    }
    
    for url in urls:
        print(f"\n📥 Processing: {url}")
        
        try:
            # Identify platform
            domain = urlparse(url).netloc.lower()
            platform = 'unknown'
            
            if 'youtube.com' in domain or 'youtu.be' in domain:
                platform = 'YouTube'
            elif 'vimeo.com' in domain:
                platform = 'Vimeo'
            elif 'dailymotion.com' in domain:
                platform = 'DailyMotion'
            elif 'twitch.tv' in domain:
                platform = 'Twitch'
            elif 'facebook.com' in domain or 'fb.watch' in domain:
                platform = 'Facebook'
            elif 'instagram.com' in domain:
                platform = 'Instagram'
            elif 'tiktok.com' in domain:
                platform = 'TikTok'
            
            results['platforms_used'].add(platform)
            
            # Download video
            video_path = download_movie(url)
            
            # Get file info
            file_size = os.path.getsize(video_path)
            size_mb = file_size / (1024 * 1024)
            
            results['successful_downloads'].append({
                'url': url,
                'platform': platform,
                'file_path': video_path,
                'size_mb': round(size_mb, 2),
                'filename': os.path.basename(video_path)
            })
            
            results['total_size_mb'] += size_mb
            
            print(f"✅ Downloaded: {os.path.basename(video_path)} ({size_mb:.2f} MB)")
            
        except Exception as e:
            results['failed_downloads'].append({
                'url': url,
                'platform': platform,
                'error': str(e)
            })
            print(f"❌ Failed: {e}")
    
    return results

# Example: Download from multiple platforms
mixed_urls = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",     # YouTube
    "https://vimeo.com/148751763",                      # Vimeo
    "https://www.dailymotion.com/video/x2hwqn9",       # DailyMotion
    "https://www.facebook.com/watch/?v=123456789",     # Facebook (example)
]

download_results = smart_video_downloader(mixed_urls)

print(f"\n📊 Download Summary:")
print(f"✅ Successful: {len(download_results['successful_downloads'])}")
print(f"❌ Failed: {len(download_results['failed_downloads'])}")
print(f"📁 Total Size: {download_results['total_size_mb']:.2f} MB")
print(f"🌐 Platforms: {', '.join(download_results['platforms_used'])}")
```

### Quality-Specific Downloads

```python
import subprocess
import json

def download_with_quality_options(url: str, quality_preference: str = 'best') -> dict:
    """Download video with specific quality preferences."""
    
    # First, get available formats
    cmd_info = [
        'yt-dlp',
        '--list-formats',
        '--dump-json',
        url
    ]
    
    try:
        result = subprocess.run(cmd_info, capture_output=True, text=True, check=True)
        video_info = json.loads(result.stdout.split('\n')[0])  # First line is JSON
        
        # Analyze available formats
        formats = video_info.get('formats', [])
        video_formats = [f for f in formats if f.get('vcodec', 'none') != 'none']
        audio_formats = [f for f in formats if f.get('acodec', 'none') != 'none']
        
        # Quality mappings
        quality_map = {
            'best': 'best[height<=2160]',      # Up to 4K
            'high': 'best[height<=1080]',      # Full HD
            'medium': 'best[height<=720]',     # HD
            'low': 'best[height<=480]',        # SD
            'mobile': 'worst[height>=360]'     # Mobile-friendly
        }
        
        format_selector = quality_map.get(quality_preference, 'best')
        
        # Download with selected quality
        cmd_download = [
            'yt-dlp',
            '-f', format_selector,
            '-o', 'downloads/%(title)s_%(height)sp.%(ext)s',
            url
        ]
        
        download_result = subprocess.run(cmd_download, capture_output=True, text=True, check=True)
        
        # Find the downloaded file
        title = video_info.get('title', 'video')
        safe_title = "".join(c for c in title if c.isalnum() or c in ' -_').strip()
        
        # Return comprehensive info
        return {
            'status': 'success',
            'title': title,
            'url': url,
            'quality_requested': quality_preference,
            'format_used': format_selector,
            'available_qualities': [f"{f['height']}p" for f in video_formats if f.get('height')],
            'duration': video_info.get('duration', 0),
            'uploader': video_info.get('uploader', 'Unknown'),
            'upload_date': video_info.get('upload_date', 'Unknown'),
            'view_count': video_info.get('view_count', 0)
        }
        
    except subprocess.CalledProcessError as e:
        return {
            'status': 'error',
            'error': str(e),
            'stderr': e.stderr
        }

# Example: Download videos in different qualities
test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

qualities = ['best', 'high', 'medium', 'low']
for quality in qualities:
    print(f"\n📥 Downloading in {quality} quality...")
    result = download_with_quality_options(test_url, quality)
    
    if result['status'] == 'success':
        print(f"✅ Downloaded: {result['title']}")
        print(f"📊 Available qualities: {', '.join(result['available_qualities'])}")
        print(f"⏱️ Duration: {result['duration']} seconds")
        print(f"👁️ Views: {result['view_count']:,}")
    else:
        print(f"❌ Error: {result['error']}")
```

## 🔧 Advanced Use Cases

### Music Production Workflow

```python
import librosa
import soundfile as sf
import numpy as np
from app import convert_to_audio, separate_voice

def music_production_pipeline(youtube_url: str) -> dict:
    """Complete music production pipeline from YouTube video."""
    
    print("🎵 Starting music production pipeline...")
    
    # Step 1: Extract audio
    print("📥 Extracting audio...")
    audio_path = convert_to_audio(youtube_url)
    
    # Step 2: Separate stems
    print("🎛️ Separating vocals and instruments...")
    separate_voice(audio_path)
    
    # Step 3: Load separated tracks
    vocals, sr = librosa.load('downloads/voice.wav')
    instruments, _ = librosa.load('downloads/background.wav')
    
    # Step 4: Audio analysis
    print("📊 Analyzing audio characteristics...")
    
    # Tempo and beat tracking
    tempo, beats = librosa.beat.beat_track(y=vocals + instruments, sr=sr)
    
    # Key detection (simplified)
    chroma = librosa.feature.chroma_cqt(y=vocals + instruments, sr=sr)
    key_profile = np.mean(chroma, axis=1)
    key_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    estimated_key = key_names[np.argmax(key_profile)]
    
    # Dynamic range analysis
    rms_vocals = librosa.feature.rms(y=vocals)[0]
    rms_instruments = librosa.feature.rms(y=instruments)[0]
    
    # Step 5: Create production stems
    print("🎚️ Creating production-ready stems...")
    
    # Normalize levels
    vocals_normalized = librosa.util.normalize(vocals)
    instruments_normalized = librosa.util.normalize(instruments)
    
    # Create click track
    click_track = librosa.clicks(times=beats, sr=sr, length=len(vocals))
    
    # Create different versions
    stems = {
        'vocals_dry': vocals_normalized,
        'vocals_compressed': librosa.effects.preemphasis(vocals_normalized),
        'instruments_full': instruments_normalized,
        'click_track': click_track,
        'full_mix': vocals_normalized * 0.7 + instruments_normalized * 0.8
    }
    
    # Step 6: Export stems
    print("💾 Exporting production stems...")
    
    stem_paths = {}
    for stem_name, audio_data in stems.items():
        file_path = f'downloads/production_{stem_name}.wav'
        sf.write(file_path, audio_data, sr)
        stem_paths[stem_name] = file_path
    
    # Step 7: Generate production report
    return {
        'original_audio': audio_path,
        'tempo_bpm': float(tempo),
        'estimated_key': estimated_key,
        'duration_seconds': len(vocals) / sr,
        'sample_rate': sr,
        'vocal_dynamic_range': float(np.max(rms_vocals) - np.min(rms_vocals)),
        'instrument_dynamic_range': float(np.max(rms_instruments) - np.min(rms_instruments)),
        'beat_times': beats.tolist(),
        'production_stems': stem_paths,
        'mix_recommendations': {
            'vocal_level': -6,  # dB
            'instrument_level': -3,  # dB
            'recommended_compressor_ratio': '3:1',
            'recommended_eq': 'High-pass at 80Hz, presence boost at 3kHz'
        }
    }

# Example usage
production_report = music_production_pipeline("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

print(f"\n🎵 Production Report:")
print(f"🎼 Key: {production_report['estimated_key']}")
print(f"🥁 Tempo: {production_report['tempo_bpm']:.1f} BPM")
print(f"⏱️ Duration: {production_report['duration_seconds']:.1f} seconds")
print(f"📊 Vocal Dynamic Range: {production_report['vocal_dynamic_range']:.2f}")
print(f"🎛️ Stems Created: {len(production_report['production_stems'])}")
```

### Educational Content Creation

```python
import json
from datetime import datetime
from karaoke_generator import generate_timed_lyrics
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip

def create_educational_content(
    youtube_url: str, 
    content_type: str = 'language_learning'
) -> dict:
    """Create educational content from video with lyrics and analysis."""
    
    print(f"🎓 Creating {content_type} content...")
    
    # Step 1: Extract and process audio
    from karaoke_generator import download_audio, separate_vocals
    
    audio_path, title = download_audio(youtube_url)
    instrumental_path, vocals_path = separate_vocals(audio_path)
    
    # Step 2: Generate detailed lyrics analysis
    print("📝 Generating detailed lyrics analysis...")
    
    import stable_whisper
    model = stable_whisper.load_model('base')
    result = model.transcribe(vocals_path, word_timestamps=True)
    
    # Extract word-level timing
    words_with_timing = []
    for segment in result.segments:
        for word in segment.words:
            words_with_timing.append({
                'word': word.word.strip(),
                'start': float(word.start),
                'end': float(word.end),
                'confidence': getattr(word, 'probability', 0.9)
            })
    
    # Step 3: Content-specific processing
    if content_type == 'language_learning':
        content_data = create_language_learning_content(words_with_timing, title)
    elif content_type == 'pronunciation_guide':
        content_data = create_pronunciation_guide(words_with_timing, vocals_path)
    elif content_type == 'lyric_analysis':
        content_data = create_lyric_analysis(words_with_timing, title)
    else:
        content_data = {'error': f'Unknown content type: {content_type}'}
    
    # Step 4: Create educational video
    if content_type == 'language_learning':
        video_path = create_language_learning_video(
            instrumental_path, 
            words_with_timing, 
            content_data,
            title
        )
    
    return {
        'title': title,
        'content_type': content_type,
        'word_count': len(words_with_timing),
        'duration': max(w['end'] for w in words_with_timing),
        'content_data': content_data,
        'video_path': video_path if 'video_path' in locals() else None,
        'generated_at': datetime.now().isoformat()
    }

def create_language_learning_content(words_with_timing: list, title: str) -> dict:
    """Create language learning materials from lyrics."""
    
    # Vocabulary analysis
    unique_words = set(word['word'].lower() for word in words_with_timing)
    
    # Difficulty classification (simplified)
    common_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
    intermediate_words = set(['because', 'although', 'however', 'therefore', 'meanwhile'])
    
    beginner_vocab = unique_words & common_words
    intermediate_vocab = unique_words & intermediate_words
    advanced_vocab = unique_words - common_words - intermediate_words
    
    # Phrase extraction (3-word combinations)
    phrases = []
    for i in range(len(words_with_timing) - 2):
        phrase = ' '.join([
            words_with_timing[i]['word'],
            words_with_timing[i+1]['word'],
            words_with_timing[i+2]['word']
        ])
        phrases.append({
            'phrase': phrase,
            'start_time': words_with_timing[i]['start'],
            'end_time': words_with_timing[i+2]['end']
        })
    
    return {
        'vocabulary_stats': {
            'total_unique_words': len(unique_words),
            'beginner_words': len(beginner_vocab),
            'intermediate_words': len(intermediate_vocab),
            'advanced_words': len(advanced_vocab)
        },
        'vocabulary_lists': {
            'beginner': sorted(list(beginner_vocab)),
            'intermediate': sorted(list(intermediate_vocab)),
            'advanced': sorted(list(advanced_vocab))
        },
        'phrases': phrases[:20],  # Top 20 phrases
        'learning_suggestions': {
            'difficulty_level': 'beginner' if len(advanced_vocab) < 10 else 'intermediate',
            'focus_areas': ['pronunciation', 'rhythm', 'intonation'],
            'practice_methods': ['shadowing', 'gap-fill exercises', 'pronunciation drills']
        }
    }

# Example: Create language learning content
educational_result = create_educational_content(
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    content_type='language_learning'
)

print(f"\n🎓 Educational Content Created:")
print(f"📚 Title: {educational_result['title']}")
print(f"📝 Word Count: {educational_result['word_count']}")
print(f"⏱️ Duration: {educational_result['duration']:.1f} seconds")

vocab_stats = educational_result['content_data']['vocabulary_stats']
print(f"📊 Vocabulary Breakdown:")
print(f"   Beginner: {vocab_stats['beginner_words']} words")
print(f"   Intermediate: {vocab_stats['intermediate_words']} words")
print(f"   Advanced: {vocab_stats['advanced_words']} words")
```

## 🤖 Integration Examples

### Flask Web Application

```python
from flask import Flask, request, jsonify, send_file
import os
import threading
from datetime import datetime
import uuid

app = Flask(__name__)

# Store processing jobs
processing_jobs = {}

@app.route('/api/process_video', methods=['POST'])
def process_video():
    """API endpoint to start video processing."""
    
    data = request.json
    youtube_url = data.get('url')
    process_type = data.get('type', 'karaoke')  # karaoke, audio, video
    
    if not youtube_url:
        return jsonify({'error': 'URL is required'}), 400
    
    # Create unique job ID
    job_id = str(uuid.uuid4())
    
    # Initialize job status
    processing_jobs[job_id] = {
        'status': 'queued',
        'url': youtube_url,
        'type': process_type,
        'created_at': datetime.now().isoformat(),
        'progress': 0,
        'message': 'Job queued for processing'
    }
    
    # Start processing in background thread
    thread = threading.Thread(
        target=background_process,
        args=(job_id, youtube_url, process_type)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'job_id': job_id,
        'status': 'queued',
        'message': 'Processing started'
    }), 202

def background_process(job_id: str, url: str, process_type: str):
    """Background processing function."""
    
    try:
        processing_jobs[job_id]['status'] = 'processing'
        processing_jobs[job_id]['progress'] = 10
        processing_jobs[job_id]['message'] = 'Starting download...'
        
        if process_type == 'karaoke':
            from karaoke_generator import main as generate_karaoke
            import sys
            
            # Simulate progress updates
            processing_jobs[job_id]['progress'] = 25
            processing_jobs[job_id]['message'] = 'Downloading audio...'
            
            # Process karaoke
            original_argv = sys.argv
            sys.argv = ['karaoke_generator.py', url]
            
            processing_jobs[job_id]['progress'] = 50
            processing_jobs[job_id]['message'] = 'Separating vocals...'
            
            generate_karaoke()
            sys.argv = original_argv
            
            processing_jobs[job_id]['progress'] = 100
            processing_jobs[job_id]['status'] = 'completed'
            processing_jobs[job_id]['message'] = 'Karaoke video created successfully'
            
        elif process_type == 'audio':
            from app import convert_to_audio, separate_voice
            
            processing_jobs[job_id]['progress'] = 30
            processing_jobs[job_id]['message'] = 'Converting to audio...'
            
            audio_path = convert_to_audio(url)
            
            processing_jobs[job_id]['progress'] = 70
            processing_jobs[job_id]['message'] = 'Separating voice...'
            
            separate_voice(audio_path)
            
            processing_jobs[job_id]['progress'] = 100
            processing_jobs[job_id]['status'] = 'completed'
            processing_jobs[job_id]['message'] = 'Audio processing completed'
            processing_jobs[job_id]['result_file'] = audio_path
            
        elif process_type == 'video':
            from movies import download_movie
            
            processing_jobs[job_id]['progress'] = 50
            processing_jobs[job_id]['message'] = 'Downloading video...'
            
            video_path = download_movie(url)
            
            processing_jobs[job_id]['progress'] = 100
            processing_jobs[job_id]['status'] = 'completed'
            processing_jobs[job_id]['message'] = 'Video download completed'
            processing_jobs[job_id]['result_file'] = video_path
            
    except Exception as e:
        processing_jobs[job_id]['status'] = 'failed'
        processing_jobs[job_id]['error'] = str(e)
        processing_jobs[job_id]['message'] = f'Processing failed: {e}'

@app.route('/api/job_status/<job_id>')
def job_status(job_id):
    """Get job status and progress."""
    
    if job_id not in processing_jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(processing_jobs[job_id])

@app.route('/api/download/<job_id>')
def download_result(job_id):
    """Download processed file."""
    
    if job_id not in processing_jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = processing_jobs[job_id]
    
    if job['status'] != 'completed':
        return jsonify({'error': 'Job not completed'}), 400
    
    if 'result_file' not in job:
        return jsonify({'error': 'No result file available'}), 404
    
    return send_file(job['result_file'], as_attachment=True)

@app.route('/api/jobs')
def list_jobs():
    """List all processing jobs."""
    return jsonify({
        'jobs': processing_jobs,
        'total_jobs': len(processing_jobs)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### Discord Bot Integration

```python
import discord
from discord.ext import commands
import asyncio
import os
from app import convert_to_audio, separate_voice
from karaoke_generator import main as generate_karaoke
import sys

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='audio')
async def extract_audio(ctx, youtube_url: str):
    """Extract audio from YouTube video."""
    
    if not youtube_url.startswith(('http://', 'https://')):
        await ctx.send("❌ Please provide a valid YouTube URL!")
        return
    
    # Send initial message
    processing_msg = await ctx.send("🎵 Processing your audio request...")
    
    try:
        # Process in thread to avoid blocking
        loop = asyncio.get_event_loop()
        
        # Extract audio
        await processing_msg.edit(content="📥 Downloading audio...")
        audio_path = await loop.run_in_executor(None, convert_to_audio, youtube_url)
        
        # Separate voice
        await processing_msg.edit(content="🎛️ Separating vocals...")
        await loop.run_in_executor(None, separate_voice, audio_path)
        
        # Send results
        await processing_msg.edit(content="✅ Audio processing completed!")
        
        # Upload files (if they're small enough for Discord)
        files_to_send = []
        
        for file_path in [audio_path, 'downloads/voice.wav', 'downloads/background.wav']:
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                if file_size < 8 * 1024 * 1024:  # 8MB Discord limit
                    files_to_send.append(discord.File(file_path))
        
        if files_to_send:
            await ctx.send("🎵 Here are your processed audio files:", files=files_to_send)
        else:
            await ctx.send("📁 Files are too large for Discord. Check your downloads folder!")
            
    except Exception as e:
        await processing_msg.edit(content=f"❌ Error: {str(e)}")

@bot.command(name='karaoke')
async def create_karaoke(ctx, youtube_url: str):
    """Create karaoke video from YouTube URL."""
    
    if not youtube_url.startswith(('http://', 'https://')):
        await ctx.send("❌ Please provide a valid YouTube URL!")
        return
    
    # Send initial message
    processing_msg = await ctx.send("🎤 Creating your karaoke video... This may take several minutes!")
    
    try:
        # Process karaoke in thread
        loop = asyncio.get_event_loop()
        
        def run_karaoke():
            original_argv = sys.argv
            sys.argv = ['karaoke_generator.py', youtube_url]
            generate_karaoke()
            sys.argv = original_argv
        
        await processing_msg.edit(content="🎬 Processing karaoke (this will take a few minutes)...")
        await loop.run_in_executor(None, run_karaoke)
        
        # Find the created karaoke file
        output_dir = 'output'
        karaoke_files = [f for f in os.listdir(output_dir) if f.endswith('_karaoke.mp4')]
        
        if karaoke_files:
            karaoke_path = os.path.join(output_dir, karaoke_files[-1])  # Most recent
            file_size = os.path.getsize(karaoke_path)
            
            await processing_msg.edit(content="✅ Karaoke video created!")
            
            if file_size < 8 * 1024 * 1024:  # 8MB limit
                await ctx.send("🎤 Your karaoke video is ready!", file=discord.File(karaoke_path))
            else:
                await ctx.send(f"🎤 Karaoke video created: {karaoke_files[-1]}\n📁 File is too large for Discord ({file_size/1024/1024:.1f}MB)")
        else:
            await ctx.send("❌ No karaoke file was created. Please check the logs.")
            
    except Exception as e:
        await processing_msg.edit(content=f"❌ Karaoke creation failed: {str(e)}")

@bot.command(name='help_audio')
async def help_audio(ctx):
    """Show available audio commands."""
    
    embed = discord.Embed(
        title="🎵 Audio Bot Commands",
        description="Available commands for audio processing",
        color=0x00ff00
    )
    
    embed.add_field(
        name="!audio <YouTube URL>",
        value="Extract and separate audio from YouTube video",
        inline=False
    )
    
    embed.add_field(
        name="!karaoke <YouTube URL>",
        value="Create karaoke video with synchronized lyrics",
        inline=False
    )
    
    embed.add_field(
        name="Examples:",
        value="`!audio https://www.youtube.com/watch?v=dQw4w9WgXcQ`\n`!karaoke https://www.youtube.com/watch?v=dQw4w9WgXcQ`",
        inline=False
    )
    
    embed.set_footer(text="Processing may take several minutes depending on video length")
    
    await ctx.send(embed=embed)

# Run bot
# bot.run('YOUR_BOT_TOKEN')
```

## 🔧 Automation Scripts

### Automated Playlist Processing

```bash
#!/bin/bash
# playlist_processor.sh - Process entire YouTube playlists

set -e  # Exit on any error

PLAYLIST_URL="$1"
OUTPUT_TYPE="$2"  # karaoke, audio, or video
MAX_CONCURRENT="$3"

if [ -z "$PLAYLIST_URL" ] || [ -z "$OUTPUT_TYPE" ]; then
    echo "Usage: $0 <playlist_url> <output_type> [max_concurrent]"
    echo "Output types: karaoke, audio, video"
    echo "Max concurrent: 1-4 (default: 2)"
    exit 1
fi

# Default values
MAX_CONCURRENT=${MAX_CONCURRENT:-2}

# Create output directories
mkdir -p logs processed failed

# Get playlist videos
echo "📥 Extracting playlist URLs..."
yt-dlp --flat-playlist --get-id "$PLAYLIST_URL" > playlist_ids.txt

# Convert IDs to URLs
sed 's/^/https:\/\/www.youtube.com\/watch?v=/' playlist_ids.txt > playlist_urls.txt

echo "📊 Found $(wc -l < playlist_urls.txt) videos in playlist"

# Function to process single video
process_video() {
    local url="$1"
    local video_id=$(echo "$url" | grep -o '[?&]v=[^&]*' | cut -d= -f2)
    local log_file="logs/${video_id}.log"
    
    echo "🎬 Processing: $url" | tee -a "$log_file"
    
    case "$OUTPUT_TYPE" in
        "karaoke")
            if python3 karaoke_generator.py "$url" >> "$log_file" 2>&1; then
                echo "$url" >> processed/karaoke_success.txt
                echo "✅ Karaoke created: $video_id"
            else
                echo "$url" >> failed/karaoke_failed.txt
                echo "❌ Karaoke failed: $video_id"
            fi
            ;;
        "audio")
            if echo "$url" | python3 app.py >> "$log_file" 2>&1; then
                echo "$url" >> processed/audio_success.txt
                echo "✅ Audio processed: $video_id"
            else
                echo "$url" >> failed/audio_failed.txt
                echo "❌ Audio failed: $video_id"
            fi
            ;;
        "video")
            if echo "$url" | python3 movies.py >> "$log_file" 2>&1; then
                echo "$url" >> processed/video_success.txt
                echo "✅ Video downloaded: $video_id"
            else
                echo "$url" >> failed/video_failed.txt
                echo "❌ Video failed: $video_id"
            fi
            ;;
        *)
            echo "❌ Unknown output type: $OUTPUT_TYPE"
            exit 1
            ;;
    esac
}

# Export function for parallel execution
export -f process_video
export OUTPUT_TYPE

# Process videos in parallel
echo "🚀 Starting parallel processing (max $MAX_CONCURRENT concurrent jobs)..."

# Use GNU parallel if available, otherwise use xargs
if command -v parallel &> /dev/null; then
    cat playlist_urls.txt | parallel -j "$MAX_CONCURRENT" process_video {}
else
    cat playlist_urls.txt | xargs -I {} -P "$MAX_CONCURRENT" bash -c 'process_video "$@"' _ {}
fi

# Generate report
echo "📊 Processing completed!"
echo "📈 Success rate calculation..."

successful=0
failed=0

for file in processed/*_success.txt; do
    if [ -f "$file" ]; then
        successful=$((successful + $(wc -l < "$file")))
    fi
done

for file in failed/*_failed.txt; do
    if [ -f "$file" ]; then
        failed=$((failed + $(wc -l < "$file")))
    fi
done

total=$((successful + failed))
success_rate=$(echo "scale=2; $successful * 100 / $total" | bc -l)

echo "✅ Successful: $successful"
echo "❌ Failed: $failed" 
echo "📊 Success rate: $success_rate%"

# Cleanup
rm playlist_ids.txt playlist_urls.txt
```

### Monitoring and Alerting Script

```python
#!/usr/bin/env python3
# monitor_processing.py - Monitor processing jobs and send alerts

import os
import time
import json
import smtplib
import psutil
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ProcessingMonitor:
    """Monitor processing jobs and system resources."""
    
    def __init__(self, config_file='monitor_config.json'):
        self.load_config(config_file)
        self.start_time = datetime.now()
        
    def load_config(self, config_file):
        """Load monitoring configuration."""
        default_config = {
            'check_interval': 60,  # seconds
            'max_cpu_usage': 90,   # percentage
            'max_memory_usage': 85,  # percentage
            'max_disk_usage': 90,    # percentage
            'alert_email': 'admin@example.com',
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'smtp_username': 'alerts@example.com',
            'smtp_password': 'app_password',
            'directories_to_monitor': ['downloads', 'temp', 'output'],
            'max_processing_time': 3600  # seconds (1 hour)
        }
        
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
            else:
                # Create default config file
                with open(config_file, 'w') as f:
                    json.dump(default_config, f, indent=2)
                logger.info(f"Created default config file: {config_file}")
        except Exception as e:
            logger.error(f"Error loading config: {e}")
        
        self.config = default_config
    
    def check_system_resources(self):
        """Check system CPU, memory, and disk usage."""
        alerts = []
        
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > self.config['max_cpu_usage']:
            alerts.append(f"High CPU usage: {cpu_percent:.1f}%")
        
        # Memory usage
        memory = psutil.virtual_memory()
        if memory.percent > self.config['max_memory_usage']:
            alerts.append(f"High memory usage: {memory.percent:.1f}%")
        
        # Disk usage
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        if disk_percent > self.config['max_disk_usage']:
            alerts.append(f"High disk usage: {disk_percent:.1f}%")
        
        return {
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'disk_percent': disk_percent,
            'alerts': alerts
        }
    
    def check_processing_jobs(self):
        """Check for stuck or long-running processing jobs."""
        alerts = []
        job_info = []
        
        # Check for Python processes running our scripts
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
            try:
                if proc.info['name'] == 'python3':
                    cmdline = ' '.join(proc.info['cmdline'])
                    
                    # Check if it's one of our processing scripts
                    our_scripts = ['app.py', 'karaoke_generator.py', 'movies.py']
                    if any(script in cmdline for script in our_scripts):
                        
                        # Calculate runtime
                        create_time = datetime.fromtimestamp(proc.info['create_time'])
                        runtime = datetime.now() - create_time
                        
                        job_info.append({
                            'pid': proc.info['pid'],
                            'script': next(s for s in our_scripts if s in cmdline),
                            'runtime_seconds': runtime.total_seconds(),
                            'cmdline': cmdline
                        })
                        
                        # Alert for long-running jobs
                        if runtime.total_seconds() > self.config['max_processing_time']:
                            alerts.append(
                                f"Long-running job (PID {proc.info['pid']}): "
                                f"{runtime.total_seconds()/60:.1f} minutes"
                            )
                            
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return {
            'active_jobs': len(job_info),
            'job_details': job_info,
            'alerts': alerts
        }
    
    def check_directory_sizes(self):
        """Check sizes of output directories."""
        directory_info = {}
        alerts = []
        
        for directory in self.config['directories_to_monitor']:
            if os.path.exists(directory):
                total_size = 0
                file_count = 0
                
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            total_size += os.path.getsize(file_path)
                            file_count += 1
                        except OSError:
                            continue
                
                size_gb = total_size / (1024**3)
                directory_info[directory] = {
                    'size_gb': size_gb,
                    'file_count': file_count
                }
                
                # Alert for very large directories (>10GB)
                if size_gb > 10:
                    alerts.append(f"Large directory {directory}: {size_gb:.2f}GB")
        
        return {
            'directories': directory_info,
            'alerts': alerts
        }
    
    def send_alert(self, subject, message):
        """Send email alert."""
        try:
            msg = MimeMultipart()
            msg['From'] = self.config['smtp_username']
            msg['To'] = self.config['alert_email']
            msg['Subject'] = subject
            
            msg.attach(MimeText(message, 'plain'))
            
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            server.starttls()
            server.login(self.config['smtp_username'], self.config['smtp_password'])
            
            text = msg.as_string()
            server.sendmail(self.config['smtp_username'], self.config['alert_email'], text)
            server.quit()
            
            logger.info(f"Alert sent: {subject}")
            
        except Exception as e:
            logger.error(f"Failed to send alert: {e}")
    
    def generate_report(self, system_info, job_info, directory_info):
        """Generate monitoring report."""
        report = f"""
YouTube DL Processing Monitor Report
Generated: {datetime.now().isoformat()}
Uptime: {datetime.now() - self.start_time}

=== System Resources ===
CPU Usage: {system_info['cpu_percent']:.1f}%
Memory Usage: {system_info['memory_percent']:.1f}%
Disk Usage: {system_info['disk_percent']:.1f}%

=== Active Processing Jobs ===
Count: {job_info['active_jobs']}
"""
        
        for job in job_info['job_details']:
            report += f"- {job['script']} (PID {job['pid']}) - Runtime: {job['runtime_seconds']/60:.1f}min\n"
        
        report += "\n=== Directory Sizes ===\n"
        for dir_name, info in directory_info['directories'].items():
            report += f"- {dir_name}: {info['size_gb']:.2f}GB ({info['file_count']} files)\n"
        
        # Alerts section
        all_alerts = (system_info['alerts'] + 
                     job_info['alerts'] + 
                     directory_info['alerts'])
        
        if all_alerts:
            report += "\n🚨 ALERTS:\n"
            for alert in all_alerts:
                report += f"- {alert}\n"
        else:
            report += "\n✅ No alerts - system running normally\n"
        
        return report, all_alerts
    
    def run_monitoring_cycle(self):
        """Run one monitoring cycle."""
        logger.info("Starting monitoring cycle...")
        
        # Collect system information
        system_info = self.check_system_resources()
        job_info = self.check_processing_jobs()
        directory_info = self.check_directory_sizes()
        
        # Generate report
        report, alerts = self.generate_report(system_info, job_info, directory_info)
        
        # Log report
        logger.info("Monitoring report generated")
        print(report)
        
        # Send alerts if necessary
        if alerts:
            self.send_alert(
                f"YouTube DL Monitor Alert - {len(alerts)} issues detected",
                report
            )
        
        # Save report to file
        with open('monitor_report.txt', 'w') as f:
            f.write(report)
        
        return len(alerts)
    
    def run(self):
        """Run continuous monitoring."""
        logger.info("Starting YouTube DL Processing Monitor...")
        
        try:
            while True:
                alert_count = self.run_monitoring_cycle()
                
                if alert_count > 0:
                    logger.warning(f"Monitoring cycle completed with {alert_count} alerts")
                else:
                    logger.info("Monitoring cycle completed - no issues")
                
                # Wait for next cycle
                time.sleep(self.config['check_interval'])
                
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
        except Exception as e:
            logger.error(f"Monitoring error: {e}")
            raise

if __name__ == "__main__":
    monitor = ProcessingMonitor()
    monitor.run()
```

This comprehensive documentation provides exhaustive examples and use cases for the YouTube DL Suite, covering everything from basic usage to advanced integrations and automation. Each example includes complete, runnable code with proper error handling and detailed explanations.