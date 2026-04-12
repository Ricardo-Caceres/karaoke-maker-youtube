# 📚 API Reference

Complete API documentation for the YouTube DL Audio & Video Processing Suite.

## 📋 Table of Contents

- [Overview](#overview)
- [Module: app.py](#module-apppy)
- [Module: karaoke_generator.py](#module-karaoke_generatorpy)
- [Module: movies.py](#module-moviespy)
- [Error Handling](#error-handling)
- [Configuration Classes](#configuration-classes)
- [Utility Functions](#utility-functions)
- [Examples](#examples)

## 🎯 Overview

This API reference provides detailed documentation for all public functions, classes, and methods in the YouTube DL suite. Each module is designed to be both standalone and integrable with other components.

### Import Structure
```python
# Individual module imports
from app import convert_to_audio, separate_voice
from movies import download_movie
from karaoke_generator import (
    download_audio, 
    separate_vocals, 
    generate_timed_lyrics, 
    create_karaoke_video
)
```

### Common Types
```python
from typing import Dict, List, Tuple, Optional, Union
from pathlib import Path

# Type aliases
URLString = str
FilePath = Union[str, Path]
AudioFormat = str  # 'mp3', 'wav', 'flac'
VideoFormat = str  # 'mp4', 'mkv', 'avi'
```

---

## 🎵 Module: app.py

Audio processing module for YouTube video conversion and voice separation.

### Functions

#### `convert_to_audio(url: str) -> str`

Converts a YouTube video to high-quality audio file.

**Parameters:**
- `url` (str): YouTube video URL

**Returns:**
- `str`: Path to the downloaded audio file

**Raises:**
- `yt_dlp.DownloadError`: If video download fails
- `OSError`: If file system operations fail
- `ValueError`: If URL is invalid

**Example:**
```python
from app import convert_to_audio

try:
    audio_path = convert_to_audio("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    print(f"Audio saved to: {audio_path}")
except Exception as e:
    print(f"Error: {e}")
```

**Configuration:**
```python
# Internal configuration (modify in source)
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',      # Format: mp3, wav, flac
        'preferredquality': '192',    # Quality: 96, 128, 192, 320
    }],
    'outtmpl': 'downloads/%(title)s.%(ext)s'
}
```

#### `separate_voice(audio_file: str) -> None`

Separates vocals from background music using harmonic-percussive separation.

**Parameters:**
- `audio_file` (str): Path to input audio file

**Returns:**
- `None`: Files are saved to downloads/ directory

**Side Effects:**
- Creates `downloads/voice.wav` - isolated vocals
- Creates `downloads/background.wav` - background music

**Raises:**
- `librosa.LibrosaError`: If audio loading/processing fails
- `soundfile.LibsndfileError`: If audio saving fails
- `FileNotFoundError`: If input file doesn't exist

**Example:**
```python
from app import separate_voice

try:
    separate_voice("downloads/song.mp3")
    print("✅ Voice separation complete")
    print("📁 Check downloads/voice.wav and downloads/background.wav")
except FileNotFoundError:
    print("❌ Audio file not found")
```

**Technical Details:**
- **Algorithm**: Harmonic-Percussive Source Separation (HPSS)
- **Quality**: Good for music with clear separation between vocals and instruments
- **Limitations**: May not work well with heavily processed or synthesized music

#### `download_audio(audio_file: str) -> bytes`

Reads audio file content into memory.

**Parameters:**
- `audio_file` (str): Path to audio file

**Returns:**
- `bytes`: Raw audio file content

**Raises:**
- `FileNotFoundError`: If file doesn't exist
- `PermissionError`: If file cannot be read

**Example:**
```python
from app import download_audio

audio_data = download_audio("downloads/song.mp3")
print(f"Audio size: {len(audio_data)} bytes")

# Save to different location
with open("backup/song.mp3", "wb") as f:
    f.write(audio_data)
```

---

## 🎤 Module: karaoke_generator.py

Professional karaoke video generation with AI-powered lyrics synchronization.

### Functions

#### `download_audio(youtube_url: str, output_path: str = "temp") -> Tuple[str, str]`

Downloads audio from YouTube video with metadata extraction.

**Parameters:**
- `youtube_url` (str): YouTube video URL
- `output_path` (str, optional): Output directory. Defaults to "temp"

**Returns:**
- `Tuple[str, str]`: (audio_filename, song_title)

**Raises:**
- `subprocess.CalledProcessError`: If yt-dlp command fails
- `FileNotFoundError`: If output directory cannot be created
- `ValueError`: If URL is invalid

**Example:**
```python
from karaoke_generator import download_audio

try:
    audio_file, title = download_audio(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        output_path="my_audio"
    )
    print(f"Downloaded: {title}")
    print(f"File: {audio_file}")
except subprocess.CalledProcessError as e:
    print(f"Download failed: {e}")
```

**Technical Details:**
- **Format**: MP3, 192kbps
- **Filename Sanitization**: Removes special characters for filesystem compatibility
- **Metadata Preservation**: Extracts title, duration, and other info

#### `separate_vocals(audio_path: str, output_path: str = "temp") -> Tuple[str, str]`

Advanced vocal separation using Spleeter AI model.

**Parameters:**
- `audio_path` (str): Path to input audio file
- `output_path` (str, optional): Output directory. Defaults to "temp"

**Returns:**
- `Tuple[str, str]`: (instrumental_path, vocals_path)

**Raises:**
- `FileNotFoundError`: If Spleeter executable not found
- `subprocess.CalledProcessError`: If separation process fails

**Example:**
```python
from karaoke_generator import separate_vocals

try:
    instrumental, vocals = separate_vocals("temp/song.mp3")
    print(f"Instrumental: {instrumental}")
    print(f"Vocals: {vocals}")
except FileNotFoundError:
    print("❌ Spleeter not installed or not found")
```

**Spleeter Models:**
- **2stems**: vocals/accompaniment (default)
- **4stems**: vocals/drums/bass/other
- **5stems**: vocals/drums/bass/piano/other

**Quality Comparison:**
```python
# Model quality vs speed tradeoff
models = {
    '2stems': {'quality': 'good', 'speed': 'fast', 'size': '150MB'},
    '4stems': {'quality': 'better', 'speed': 'medium', 'size': '300MB'},
    '5stems': {'quality': 'best', 'speed': 'slow', 'size': '500MB'}
}
```

#### `generate_timed_lyrics(vocals_path: str) -> List[Dict[str, Union[str, float]]]`

Generates time-synchronized lyrics using Whisper AI.

**Parameters:**
- `vocals_path` (str): Path to vocals audio file

**Returns:**
- `List[Dict]`: List of lyrics segments with timing
  ```python
  [
      {
          'text': 'Never gonna give you up',
          'start': 15.2,  # seconds
          'end': 18.7     # seconds
      },
      # ... more segments
  ]
  ```

**Raises:**
- `Exception`: If Whisper model loading fails
- `RuntimeError`: If transcription process fails

**Example:**
```python
from karaoke_generator import generate_timed_lyrics

try:
    lyrics = generate_timed_lyrics("temp/vocals.wav")
    
    for segment in lyrics[:3]:  # First 3 segments
        print(f"{segment['start']:.1f}s - {segment['end']:.1f}s: {segment['text']}")
        
    print(f"Total segments: {len(lyrics)}")
except Exception as e:
    print(f"Transcription failed: {e}")
```

**Whisper Models:**
```python
models = {
    'tiny': {'size': '39MB', 'speed': 'fastest', 'accuracy': 'lowest'},
    'base': {'size': '74MB', 'speed': 'fast', 'accuracy': 'good'},      # Default
    'small': {'size': '244MB', 'speed': 'medium', 'accuracy': 'better'},
    'medium': {'size': '769MB', 'speed': 'slow', 'accuracy': 'high'},
    'large': {'size': '1550MB', 'speed': 'slowest', 'accuracy': 'highest'}
}
```

**Customization Options:**
```python
# Modify in source code for custom behavior
MAX_WORDS_PER_LINE = 8      # Words per subtitle line
MIN_SEGMENT_DURATION = 1.0  # Minimum segment length in seconds
MAX_SEGMENT_DURATION = 5.0  # Maximum segment length in seconds
```

#### `create_karaoke_video(instrumental_path: str, timed_lyrics: List[Dict], song_title: str, output_path: str = "output") -> None`

Creates professional karaoke video with synchronized lyrics overlay.

**Parameters:**
- `instrumental_path` (str): Path to instrumental audio track
- `timed_lyrics` (List[Dict]): Time-synchronized lyrics from `generate_timed_lyrics()`
- `song_title` (str): Title for output filename
- `output_path` (str, optional): Output directory. Defaults to "output"

**Returns:**
- `None`: Video file is saved to output directory

**Raises:**
- `Exception`: If video creation process fails
- `MemoryError`: If system runs out of memory during processing

**Example:**
```python
from karaoke_generator import create_karaoke_video

# Assuming you have the required inputs
instrumental = "temp/song/accompaniment.wav"
lyrics = [
    {'text': 'Hello world', 'start': 0.0, 'end': 2.0},
    {'text': 'This is karaoke', 'start': 2.5, 'end': 5.0}
]
title = "My Karaoke Song"

try:
    create_karaoke_video(instrumental, lyrics, title)
    print("✅ Karaoke video created successfully!")
except MemoryError:
    print("❌ Not enough memory - try shorter video or lower resolution")
```

**Video Specifications:**
```python
# Default video settings
VIDEO_CONFIG = {
    'resolution': (1280, 720),      # HD resolution
    'framerate': 30,                # FPS
    'codec': 'libx264',            # Video codec
    'audio_codec': 'aac',          # Audio codec
    'bitrate': '5M',               # Video bitrate
    'background_color': (25, 25, 112)  # Dark blue RGB
}

# Text styling
TEXT_CONFIG = {
    'font': 'Arial',
    'fontsize': 60,
    'color': 'white',
    'highlight_color': 'yellow',
    'position': ('center', 0.65),  # Horizontal, Vertical (0.0-1.0)
    'outline': 2,                  # Text outline width
    'shadow': True                 # Drop shadow
}
```

#### `main() -> None`

Command-line interface for complete karaoke generation pipeline.

**Usage:**
```bash
python3 karaoke_generator.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

**Example:**
```python
import sys
from karaoke_generator import main

# Simulate command line usage
sys.argv = ['karaoke_generator.py', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ']
main()
```

---

## 📹 Module: movies.py

High-quality video downloading from multiple platforms.

### Functions

#### `download_movie(url: str) -> str`

Downloads video in the best available quality from supported platforms.

**Parameters:**
- `url` (str): Video URL from supported platform

**Returns:**
- `str`: Path to downloaded video file

**Raises:**
- `yt_dlp.DownloadError`: If download fails
- `OSError`: If file system operations fail
- `ValueError`: If URL is unsupported

**Example:**
```python
from movies import download_movie

try:
    video_path = download_movie("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    print(f"Video downloaded to: {video_path}")
    
    # Get file info
    import os
    size_mb = os.path.getsize(video_path) / (1024 * 1024)
    print(f"File size: {size_mb:.2f} MB")
    
except Exception as e:
    print(f"Download failed: {e}")
```

**Supported Platforms:**
- YouTube
- Vimeo
- DailyMotion
- Twitch
- Facebook
- Instagram
- TikTok
- Twitter
- Reddit
- And 100+ more...

**Quality Selection:**
```python
# Internal quality preference (modify in source)
ydl_opts = {
    'format': 'best',  # Options: 'best', 'worst', 'bestvideo+bestaudio'
    'outtmpl': 'downloads/%(title)s.%(ext)s'
}

# Custom format selection examples:
formats = {
    'highest_quality': 'best[height>=1080]',
    'medium_quality': 'best[height>=720]',
    'mobile_friendly': 'worst[height>=480]',
    'audio_only': 'bestaudio/best'
}
```

---

## ⚠️ Error Handling

### Exception Hierarchy

```python
# Base exceptions
class YouTubeDLError(Exception):
    """Base exception for YouTube DL suite"""
    pass

class DownloadError(YouTubeDLError):
    """Raised when download operations fail"""
    pass

class ProcessingError(YouTubeDLError):
    """Raised when audio/video processing fails"""
    pass

class ConfigurationError(YouTubeDLError):
    """Raised when configuration is invalid"""
    pass
```

### Common Error Patterns

#### Network-Related Errors
```python
from yt_dlp import DownloadError
import requests.exceptions

def safe_download(url):
    try:
        return convert_to_audio(url)
    except DownloadError as e:
        if "HTTP Error 403" in str(e):
            print("❌ Video is private or restricted")
        elif "Video unavailable" in str(e):
            print("❌ Video has been removed")
        elif "network" in str(e).lower():
            print("❌ Network connection issue")
        else:
            print(f"❌ Download failed: {e}")
    except requests.exceptions.ConnectionError:
        print("❌ No internet connection")
```

#### File System Errors
```python
import os
from pathlib import Path

def safe_file_operation(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except PermissionError:
        print("❌ Permission denied - check file permissions")
    except FileNotFoundError:
        print("❌ File not found - check file path")
    except OSError as e:
        if e.errno == 28:  # No space left
            print("❌ Disk full - free up space")
        else:
            print(f"❌ File system error: {e}")
```

#### Processing Errors
```python
def safe_audio_processing(audio_path):
    try:
        separate_voice(audio_path)
    except librosa.LibrosaError as e:
        print(f"❌ Audio processing failed: {e}")
        print("💡 Try converting to WAV format first")
    except MemoryError:
        print("❌ Not enough memory")
        print("💡 Try processing shorter audio segments")
```

---

## 🔧 Configuration Classes

### AudioConfig

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class AudioConfig:
    """Configuration for audio processing operations"""
    
    # Quality settings
    format: str = 'mp3'              # mp3, wav, flac
    quality: str = '192'             # 96, 128, 192, 320 (kbps)
    sample_rate: int = 44100         # Hz
    channels: int = 2                # 1=mono, 2=stereo
    
    # Processing settings
    normalize_audio: bool = True      # Normalize volume
    noise_reduction: bool = False     # Apply noise reduction
    
    # Paths
    output_dir: str = 'downloads'
    temp_dir: str = 'temp'
    
    def __post_init__(self):
        """Validate configuration"""
        valid_formats = ['mp3', 'wav', 'flac', 'ogg']
        if self.format not in valid_formats:
            raise ValueError(f"Invalid format: {self.format}")
            
        if not (96 <= int(self.quality) <= 320):
            raise ValueError(f"Invalid quality: {self.quality}")

# Usage example
config = AudioConfig(format='wav', quality='320')
```

### VideoConfig

```python
@dataclass
class VideoConfig:
    """Configuration for video processing operations"""
    
    # Video settings
    resolution: tuple = (1280, 720)   # Width, Height
    framerate: int = 30               # FPS
    codec: str = 'libx264'           # Video codec
    bitrate: str = '5M'              # Video bitrate
    
    # Audio settings
    audio_codec: str = 'aac'         # Audio codec
    audio_bitrate: str = '192k'      # Audio bitrate
    
    # Styling
    background_color: tuple = (25, 25, 112)  # RGB
    font_family: str = 'Arial'
    font_size: int = 60
    text_color: str = 'white'
    highlight_color: str = 'yellow'
    
    # Paths
    output_dir: str = 'output'
    temp_dir: str = 'temp'

# Usage example
video_config = VideoConfig(
    resolution=(1920, 1080),  # Full HD
    framerate=60,             # High framerate
    font_size=80              # Larger text
)
```

### WhisperConfig

```python
@dataclass
class WhisperConfig:
    """Configuration for Whisper transcription"""
    
    model_size: str = 'base'         # tiny, base, small, medium, large
    language: Optional[str] = None    # Auto-detect if None
    fp16: bool = False               # Use half precision (GPU only)
    
    # Processing options
    beam_size: int = 5               # Beam search size
    best_of: int = 5                # Number of candidates
    temperature: float = 0.0         # Sampling temperature
    
    # Output formatting
    max_words_per_line: int = 8      # Words per subtitle line
    min_segment_duration: float = 1.0 # Minimum segment length
    max_segment_duration: float = 5.0 # Maximum segment length

# Usage example
whisper_config = WhisperConfig(
    model_size='large',      # Best accuracy
    language='en',           # English only
    fp16=True               # GPU acceleration
)
```

---

## 🛠️ Utility Functions

### File Management

```python
import os
import shutil
from pathlib import Path
from typing import List

def ensure_directory(path: str) -> Path:
    """
    Ensure directory exists, create if necessary.
    
    Args:
        path: Directory path to create
        
    Returns:
        Path object of created directory
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path

def clean_filename(filename: str) -> str:
    """
    Remove invalid characters from filename.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename safe for filesystem
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove multiple spaces and trailing periods
    filename = ' '.join(filename.split())
    filename = filename.rstrip('.')
    
    return filename[:255]  # Limit to 255 characters

def get_file_size(filepath: str) -> str:
    """
    Get human-readable file size.
    
    Args:
        filepath: Path to file
        
    Returns:
        Formatted file size string
    """
    size = os.path.getsize(filepath)
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    
    return f"{size:.1f} TB"

def cleanup_temp_files(temp_dir: str = 'temp') -> None:
    """
    Clean up temporary files and directories.
    
    Args:
        temp_dir: Temporary directory to clean
    """
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        print(f"🧹 Cleaned up {temp_dir}")
```

### Progress Tracking

```python
import time
from typing import Callable, Any

def with_progress(func: Callable) -> Callable:
    """
    Decorator to add progress tracking to functions.
    
    Args:
        func: Function to wrap with progress tracking
        
    Returns:
        Wrapped function with progress output
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(f"🚀 Starting {func.__name__}...")
        
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            print(f"✅ {func.__name__} completed in {elapsed:.2f}s")
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"❌ {func.__name__} failed after {elapsed:.2f}s: {e}")
            raise
    
    return wrapper

# Usage example
@with_progress
def download_and_process(url: str) -> str:
    audio_path = convert_to_audio(url)
    separate_voice(audio_path)
    return audio_path
```

### Validation

```python
import re
from urllib.parse import urlparse

def validate_youtube_url(url: str) -> bool:
    """
    Validate YouTube URL format.
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid YouTube URL
    """
    youtube_patterns = [
        r'https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+',
        r'https?://youtu\.be/[\w-]+',
        r'https?://(?:www\.)?youtube\.com/embed/[\w-]+',
    ]
    
    return any(re.match(pattern, url) for pattern in youtube_patterns)

def validate_audio_file(filepath: str) -> bool:
    """
    Validate audio file format and accessibility.
    
    Args:
        filepath: Path to audio file
        
    Returns:
        True if valid audio file
    """
    if not os.path.exists(filepath):
        return False
    
    valid_extensions = ['.mp3', '.wav', '.flac', '.ogg', '.m4a']
    extension = os.path.splitext(filepath)[1].lower()
    
    return extension in valid_extensions

def estimate_processing_time(audio_duration: float) -> dict:
    """
    Estimate processing times for different operations.
    
    Args:
        audio_duration: Duration of audio in seconds
        
    Returns:
        Dictionary with estimated times for each operation
    """
    # Based on benchmarking (times in seconds per minute of audio)
    base_times = {
        'download': 2.0,      # 2 seconds per minute
        'separation': 10.0,   # 10 seconds per minute  
        'transcription': 15.0, # 15 seconds per minute
        'video_creation': 20.0 # 20 seconds per minute
    }
    
    minutes = audio_duration / 60
    
    return {
        operation: minutes * time_per_minute 
        for operation, time_per_minute in base_times.items()
    }
```

---

## 💡 Examples

### Complete Karaoke Pipeline

```python
from karaoke_generator import (
    download_audio, 
    separate_vocals, 
    generate_timed_lyrics, 
    create_karaoke_video
)
from pathlib import Path
import os

def create_karaoke_from_url(youtube_url: str, output_dir: str = "output") -> str:
    """
    Complete karaoke creation pipeline.
    
    Args:
        youtube_url: YouTube video URL
        output_dir: Directory for final video
        
    Returns:
        Path to created karaoke video
    """
    
    # Ensure directories exist
    Path("temp").mkdir(exist_ok=True)
    Path(output_dir).mkdir(exist_ok=True)
    
    try:
        # Step 1: Download audio
        print("📥 Downloading audio...")
        audio_path, song_title = download_audio(youtube_url)
        
        # Step 2: Separate vocals
        print("🎵 Separating vocals...")
        instrumental_path, vocals_path = separate_vocals(audio_path)
        
        # Step 3: Generate lyrics
        print("📝 Generating lyrics...")
        timed_lyrics = generate_timed_lyrics(vocals_path)
        
        if not timed_lyrics:
            raise Exception("No lyrics could be generated")
        
        # Step 4: Create video
        print("🎬 Creating karaoke video...")
        create_karaoke_video(instrumental_path, timed_lyrics, song_title, output_dir)
        
        # Return final video path
        safe_title = "".join(c for c in song_title if c.isalnum() or c in ' -_').strip()
        video_path = os.path.join(output_dir, f"{safe_title}_karaoke.mp4")
        
        print(f"✅ Karaoke video created: {video_path}")
        return video_path
        
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        raise

# Usage
video_path = create_karaoke_from_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
```

### Batch Processing

```python
import concurrent.futures
from typing import List, Dict
import json

def batch_process_videos(urls: List[str], max_workers: int = 2) -> Dict[str, str]:
    """
    Process multiple videos in parallel.
    
    Args:
        urls: List of YouTube URLs
        max_workers: Maximum concurrent processes
        
    Returns:
        Dictionary mapping URLs to result status
    """
    
    results = {}
    
    def process_single_url(url: str) -> tuple:
        try:
            video_path = create_karaoke_from_url(url)
            return (url, f"✅ Success: {video_path}")
        except Exception as e:
            return (url, f"❌ Failed: {str(e)}")
    
    # Process URLs in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(process_single_url, url): url for url in urls}
        
        for future in concurrent.futures.as_completed(future_to_url):
            url, result = future.result()
            results[url] = result
            print(f"Completed: {url} -> {result}")
    
    # Save results
    with open('batch_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    return results

# Usage
urls = [
    "https://www.youtube.com/watch?v=VIDEO1",
    "https://www.youtube.com/watch?v=VIDEO2",
    "https://www.youtube.com/watch?v=VIDEO3"
]

results = batch_process_videos(urls, max_workers=2)
```

### Custom Video Styling

```python
from moviepy.video.VideoClip import ColorClip, TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

def create_custom_karaoke_video(
    instrumental_path: str,
    timed_lyrics: list,
    song_title: str,
    style_config: dict = None
) -> str:
    """
    Create karaoke video with custom styling.
    
    Args:
        instrumental_path: Path to instrumental audio
        timed_lyrics: Synchronized lyrics data
        song_title: Song title for filename
        style_config: Custom styling options
        
    Returns:
        Path to created video
    """
    
    # Default style configuration
    default_style = {
        'resolution': (1920, 1080),
        'background_color': (0, 0, 0),        # Black background
        'font_family': 'Arial-Bold',
        'font_size': 80,
        'text_color': 'white',
        'highlight_color': '#FFD700',          # Gold
        'subtitle_position': 0.8,              # Bottom of screen
        'fade_duration': 0.5,                  # Fade in/out time
        'outline_width': 3,
        'shadow_offset': (2, 2)
    }
    
    # Merge with user configuration
    style = {**default_style, **(style_config or {})}
    
    # Load audio
    audio_clip = AudioFileClip(instrumental_path)
    video_duration = audio_clip.duration
    
    # Create background
    background = ColorClip(
        size=style['resolution'],
        color=style['background_color'],
        duration=video_duration
    )
    
    # Create text clips with custom styling
    text_clips = []
    
    for line in timed_lyrics:
        # Main text
        text_clip = TextClip(
            txt=line['text'],
            fontsize=style['font_size'],
            color=style['text_color'],
            font=style['font_family'],
            size=(style['resolution'][0] - 100, None),
            method='caption',
            align='center',
            stroke_color='black',
            stroke_width=style['outline_width']
        ).set_position(('center', style['subtitle_position'])) \
         .set_start(line['start']) \
         .set_duration(line['end'] - line['start']) \
         .fadein(style['fade_duration']) \
         .fadeout(style['fade_duration'])
        
        text_clips.append(text_clip)
        
        # Highlight effect (optional)
        if style.get('add_highlight', True):
            highlight_clip = TextClip(
                txt=line['text'],
                fontsize=style['font_size'],
                color=style['highlight_color'],
                font=style['font_family'],
                size=(style['resolution'][0] - 100, None),
                method='caption',
                align='center'
            ).set_position(('center', style['subtitle_position'])) \
             .set_start(line['start']) \
             .set_duration(0.2) \
             .set_opacity(0.7)
            
            text_clips.append(highlight_clip)
    
    # Compose final video
    final_clip = CompositeVideoClip([background] + text_clips)
    final_clip = final_clip.set_audio(audio_clip)
    
    # Generate output filename
    safe_title = clean_filename(song_title)
    output_path = f"output/{safe_title}_custom_karaoke.mp4"
    
    # Render video
    final_clip.write_videofile(
        output_path,
        codec='libx264',
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True,
        fps=30
    )
    
    return output_path

# Usage with custom styling
custom_style = {
    'resolution': (1920, 1080),
    'background_color': (25, 25, 112),  # Navy blue
    'font_size': 100,
    'text_color': '#FFFFFF',
    'highlight_color': '#FF6B6B',       # Coral red
    'subtitle_position': 0.75,
    'add_highlight': True
}

video_path = create_custom_karaoke_video(
    "temp/song/accompaniment.wav",
    timed_lyrics,
    "My Custom Karaoke",
    custom_style
)
```

---

This comprehensive API reference provides all the information needed to integrate and extend the YouTube DL suite. Each function includes detailed parameters, return values, error conditions, and practical examples for immediate use.

For more advanced usage patterns and integration examples, refer to the main README.md file and the source code comments.